# STEP · R
# R has no per-line trace hook the way C has gdb and Python has sys.settrace,
# so this walks the parse tree itself: into `{`, `for`, `while`, `repeat` and
# `if`, recording the source line and the variable state after every statement.
# A call into a user-defined function is therefore one step, not several, and
# the stepper page says so rather than implying the three languages trace alike.
#
# Stepping into your own functions was built and then removed on 2026-08-22.
# It worked, and it fired on 0 of the 39 R solutions: in every one of them the
# call to a user function is nested inside cat() or sprintf() rather than made
# at statement level, so reaching it needs a real evaluator — lazy arguments,
# `...`, S3 dispatch — rather than a tree walk. Measured before deciding, and
# the limitation is stated on the page instead of being half-fixed.
#
# Usage: Rscript --vanilla rstep.R <src.R> <out.json> [value-char-cap]

args <- commandArgs(trailingOnly = TRUE)
SRC <- args[1]
OUT <- args[2]
CAP <- if (length(args) >= 3) as.integer(args[3]) else 200L

# ---- step buffer -----------------------------------------------------------
# Preallocated and doubled. Appending to a list 200,014 times is quadratic, and
# D6.1 executes exactly that many steps.
buf <- character(4096L)
n <- 0L

push <- function(s) {
  if (n == length(buf)) buf <<- c(buf, character(length(buf)))
  n <<- n + 1L
  buf[n] <<- s
}

# ---- value rendering -------------------------------------------------------
# str() via capture.output is correct and far too slow at this step count, so
# each shape is formatted directly.
brief <- function(v) {
  s <- tryCatch({
    if (is.data.frame(v)) {
      sprintf("data.frame %d x %d [%s]", nrow(v), ncol(v),
              paste(utils::head(names(v), 8), collapse = ", "))
    } else if (is.matrix(v)) {
      sprintf("%s matrix %d x %d [%s]", typeof(v), nrow(v), ncol(v),
              paste(format(utils::head(as.vector(v), 6), digits = 5), collapse = " "))
    } else if (is.factor(v)) {
      sprintf("factor[%d] %s", length(v),
              paste(utils::head(as.character(v), 6), collapse = " "))
    } else if (is.atomic(v)) {
      h <- paste(format(utils::head(v, 6), digits = 5), collapse = " ")
      if (length(v) == 1L) h else sprintf("%s[%d] %s%s", typeof(v), length(v), h,
                                          if (length(v) > 6L) " …" else "")
    } else if (is.list(v)) {
      sprintf("list[%d] [%s]", length(v),
              paste(utils::head(names(v), 8), collapse = ", "))
    } else {
      paste(class(v), collapse = "/")
    }
  }, error = function(e) "<unprintable>")
  s <- gsub("[\r\n\t]+", " ", s)
  if (nchar(s) > CAP) s <- paste0(substr(s, 1L, CAP), "…")
  s
}

esc <- function(s) {
  s <- gsub("\\", "\\\\", s, fixed = TRUE)
  s <- gsub("\"", "\\\"", s, fixed = TRUE)
  s
}

snap_json <- function(env) {
  nm <- ls(env, all.names = FALSE)
  if (!length(nm)) return("{}")
  out <- character(0)
  for (k in nm) {
    v <- tryCatch(get(k, envir = env), error = function(e) NULL)
    if (is.null(v) || is.function(v)) next
    out <- c(out, paste0("\"", esc(k), "\":\"", esc(brief(v)), "\""))
  }
  paste0("{", paste(out, collapse = ","), "}")
}

record <- function(line, env, fn = "top") {
  push(paste0("[", if (is.na(line)) "null" else line, ",\"", fn, "\",",
              snap_json(env), "]"))
}

# ---- the stepper -----------------------------------------------------------
# A `{` block's srcref attribute is a *list* of srcrefs, one per statement;
# every other expression carries a single srcref. Coercing the list aborts the
# run, which is what killed D6.3, D9.3, D10.2 and D11.2 in the prototype.
line_of <- function(e) {
  sr <- attr(e, "srcref")
  if (is.null(sr)) return(NA_integer_)
  if (is.list(sr)) {
    if (!length(sr)) return(NA_integer_)
    sr <- sr[[1L]]
  }
  as.integer(sr)[1L]
}

step_eval <- function(e, env, line = NA_integer_) {
  if (is.na(line)) line <- line_of(e)
  if (!is.call(e)) return(invisible(eval(e, env)))
  head <- tryCatch(as.character(e[[1L]])[1L], error = function(x) "")

  if (identical(head, "{")) {
    srl <- attr(e, "srcref")
    if (length(e) >= 2L) {
      for (i in 2:length(e)) {
        l <- if (!is.null(srl) && length(srl) >= i - 1L)
          as.integer(srl[[i - 1L]])[1L] else NA_integer_
        step_eval(e[[i]], env, l)
      }
    }
    return(invisible(NULL))
  }
  if (identical(head, "for")) {
    record(line, env)
    var <- as.character(e[[2L]])
    seqv <- eval(e[[3L]], env)
    body <- e[[4L]]
    for (val in seqv) {
      assign(var, val, envir = env)
      step_eval(body, env)
    }
    return(invisible(NULL))
  }
  if (identical(head, "while")) {
    record(line, env)
    while (isTRUE(eval(e[[2L]], env))) step_eval(e[[3L]], env)
    return(invisible(NULL))
  }
  if (identical(head, "repeat")) {
    record(line, env)
    repeat step_eval(e[[2L]], env)
    return(invisible(NULL))
  }
  if (identical(head, "if")) {
    record(line, env)
    if (isTRUE(eval(e[[2L]], env))) step_eval(e[[3L]], env)
    else if (length(e) >= 4L) step_eval(e[[4L]], env)
    return(invisible(NULL))
  }

  v <- withVisible(eval(e, env))
  if (v$visible) print(v$value)
  record(line, env)
  invisible(v$value)
}

exprs <- parse(SRC, keep.source = TRUE)
env <- new.env(parent = globalenv())
srl <- attr(exprs, "srcref")
for (i in seq_along(exprs)) {
  l <- if (!is.null(srl)) as.integer(srl[[i]])[1L] else NA_integer_
  step_eval(exprs[[i]], env, l)
}

con <- file(OUT, "w")
writeLines(paste0("{\"gran\":\"statement\",\"steps\":[",
                  paste(buf[seq_len(n)], collapse = ","), "]}"), con)
close(con)
