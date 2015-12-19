; =============
; Merge sort
; =============

(begin

	(import lib/stdlib)

	; Merges two *sorted* lists in a single one (also sorted)
	(define merge-lists (lambda (lhs rhs)
		(cond
			((null? lhs) rhs)
			((null? rhs) lhs)
			(else
				(if (>= (car lhs) (car rhs))
					(cons (car rhs) (merge-lists lhs (cdr rhs)))
					(cons (car lhs) (merge-lists (cdr lhs) rhs))
				)
			)
		)
		;
		; An alternative implementation using `if` instead of `cond`
		;
		;(if (null? lhs)
		;	rhs
		;	(if (null? rhs)
		;		lhs
		;		(if (>= (car lhs) (car rhs))
		;			(cons (car rhs) (merge-lists lhs (cdr rhs)))
		;			(cons (car lhs) (merge-lists (cdr lhs) rhs))
		;		)
		;	)
		;)
	))

	(assert (equal? (merge-lists '() '()) '()))
	(assert (equal? (merge-lists '(1) '(2)) '(1 2)))
	(assert (equal? (merge-lists '(2) '(1)) '(1 2)))
	(assert (equal? (merge-lists '(2 5 9) '(1 2 10)) '(1 2 2 5 9 10)))
	(assert (equal? (merge-lists '(2 7 100 101) '(0 5 9 12 105)) '(0 2 5 7 9 12 100 101 105)))

	; Returns the right half of a list
	(define right-half (lambda (list)
		(last list (ceiling (/ (length list) 2)))
	))

	(assert (equal? (right-half '()) '()))
	(assert (equal? (right-half '(1)) '(1)))
	(assert (equal? (right-half '(1 3 4)) '(3 4)))
	(assert (equal? (right-half '(6 5 4 3)) '(4 3)))
	(assert (equal? (right-half '(6 5 4 3 0)) '(4 3 0)))

	; Returns the left side of a list
	(define left-half (lambda (list)
		(ldiff list (right-half list))
	))

	(assert (equal? (left-half '()) '()))
	(assert (equal? (left-half '(1)) '()))
	(assert (equal? (left-half '(1 3 4)) '(1)))
	(assert (equal? (left-half '(6 5 4 3)) '(6 5)))
	(assert (equal? (left-half '(6 5 4 3 0)) '(6 5)))

	; Returns T if the given list is empty or contains just one element
	(define small (lambda (list)
		(or
			(= (length list) 0)
			(= (length list) 1)
		)
	))

	(assert (equal? (small '()) 1))
	(assert (equal? (small '(foo)) 1))
	(assert (equal? (small '(foo bar)) 0))

	; Sorts the given list using merge sort algorithm
	(define merge-sort (lambda (list)
		(if (small list)
			list ; return the list itself if it contains one or zero items
			(merge-lists ; otherwise merge the left and the right halfs (already sorted) of the list recursively
				(merge-sort (left-half list))
				(merge-sort (right-half list))
			)
		)
	))

	(assert (equal? (merge-sort '()) '()))
	(assert (equal? (merge-sort '(1)) '(1)))
	(assert (equal? (merge-sort '(1 -8 5 19 7 3 4 9)) '(-8 1 3 4 5 7 9 19)))
)
