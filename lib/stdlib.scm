; =============
; stdlib
; =============

(begin

	; ========================================================
	; COMPARATORS
	; ========================================================

	; Greater than or equal
	(define >= (lambda (lhs rhs)
		(or (> lhs rhs) (= lhs rhs))
	))

	; Less than or equal
	(define <= (lambda (lhs rhs)
		(or (< lhs rhs) (= lhs rhs))
	))

	; Returns T if the given list is empty
	(define null? (lambda (list)
		(= list '())
	))

	(define equal? (lambda (lhs rhs)
		(if (= lhs rhs) #t #f)
	))

	(define not (lambda (x)
		(if (equal? #f x) #t #f)
	))

	(assert (equal? (not #f) #t))
	(assert (equal? (not #t) #f))
	(assert (equal? (not 3) #f))
	(assert (equal? (not '(3)) #f))
	(assert (equal? (not '()) #f))

	(define min(lambda (a b)
		(if (> a b) b a)
	))

	(define max(lambda (a b)
		(if (< a b) b a)
	))

	; ========================================================
	; TYPES
	; ========================================================

	(assert (equal? (boolean? #t) #t))
	(assert (equal? (boolean? #f) #t))
	(assert (equal? (boolean? '()) #f))
	(assert (equal? (boolean? 0) #f))
	(assert (equal? (boolean? <=) #f))

	; ========================================================
	; MATH
	; ========================================================

	; Some useful constants
	(define EPS 0.000001)
	(define PI 3.141592653589793)

	; Calculates a factorial of `n`
	; n >= 0
	(define fact (lambda (n)
		(begin
			;; define a helper function for accumulating results
			(define factorial (lambda (n acc)
				(if (= n 0)
					acc
					(factorial (- n 1) (* n acc))
				)
			))
			; call the helper
			(factorial n 1)
		)
	))

	(assert (equal? (fact 0) 1))
	(assert (equal? (fact 1) 1))
	(assert (equal? (fact 6) 720))
	(assert (equal? (fact 50) 30414093201713378043612608166064768844377641568960512000000000000))

	; Returns x raised to the power of y.
	; y must be >= 0
	(define ^ (lambda (x y)
		(if (equal? y 0)
			1
			; TODO: optimize for x=0
			(if (equal? y 1)
				x
				(* x (^ x (- y 1)))
			)
		)
	))

	(assert (equal? (^ 0 0) 1))
	(assert (equal? (^ 0 9) 0))
	(assert (equal? (^ 2 0) 1))
	(assert (equal? (^ 2 1) 2))
	(assert (equal? (^ 2 10) 1024))
	(assert (equal? (^ -2 2) 4))
	(assert (equal? (^ -2 3) -8))

	; x*x, x^2
	(define square (lambda (x)
		(^ x 2)
	))

	(assert (equal? (square 2) 4))
	(assert (equal? (square -2) 4))
	(assert (equal? (square 0) 0))

	(define abs (lambda (x)
		(if (< x 0) (- 0 x) x)
	))

	(assert (equal? (abs 3) (abs -3)))
	(assert (equal? (abs 0) 0))

	; Each iteration of the algorithm improves the guess for a litle
	(define sqrt-iter (lambda (guess x)
		(if (newton-sqrt-good-enough? guess x)
			guess
			(sqrt-iter (improve-newton-sqrt-guess guess x) x)
		)
	))

	; new_guess = (old_guess + (x/old_guess)) / 2
	(define improve-newton-sqrt-guess (lambda (guess x)
		(average guess (/ x guess))
	))

	; Returns T if the difference between guess^2 and x is less than EPS
	(define newton-sqrt-good-enough? (lambda (guess x)
		(< (abs (- (square guess) x)) EPS)
	))

	; Return the average of two numbers
	(define average (lambda (x y)
		(/ (+ x y) 2)
	))

	; Returns a square root of x. Based on Newton's method.
	; x >= 0 since we don't support complex numbers (yet?)
	(define sqrt (lambda (x)
		(if (equal? x 0)
			0
			(sqrt-iter 1.0 x)
		)
	))

	(assert (and (> (sqrt 9) 3) (< (sqrt 9) (+ 3 EPS))))
	(assert (equal? (sqrt 0) 0))

	; Modulo
	(define modulo (lambda (x y)
		(- x (* y (flooring (/ x y))))
	))

	(define remainder modulo)

	(assert (equal? (modulo 0 1) 0))
	(assert (equal? (modulo 1 1) 0))
	(assert (equal? (modulo 3 2) 1))
	(assert (equal? (modulo 12 5) 2))
	(assert (equal? (modulo -12 5) 3))
	(assert (equal? (modulo 12 5) 2))
	(assert (equal? (modulo -78 33) 21))
	(assert (equal? (modulo 78 33) 12))
	(assert (equal? (modulo 5 89) 5))


	(define odd? (lambda (x)
		(equal? (abs (remainder x 2)) 1)
	))

	(assert (odd? 1))
	(assert (odd? 3))
	(assert (odd? 1813))

	(assert (not (odd? 2)))
	(assert (not (odd? 8724)))
	(assert (not (odd? 0)))

	(define even? (lambda (x)
		(equal? (abs (remainder x 2)) 0)
	))

	(assert (even? 2))
	(assert (even? 8724))
	(assert (even? 0))

	(assert (not (even? 3)))
	(assert (not (even? 8971)))
	(assert (not (even? 1)))

	; ========================================================
	; LISTS
	; ========================================================

	(define min-list(lambda (list)
		(if (= (length list) 1)
			(car list)
			(min (car list) (min-list (cdr list)))
		)
	))

	(define max-list(lambda (list)
		(if (= (length list) 1)
			(car list)
			(max (car list) (max-list (cdr list)))
		)
	))

	; ------------------
	; <reverse>
	; ------------------
	; Returns a reversed list.
	; If x isn't a list, returns x
	(define reverse (lambda (x)
		(if (or (null? x) (not (list? x)))
			x
			(cons (reverse (cdr x)) (car x))
		)
	))

	(assert (equal? (reverse '()) '()))
	(assert (equal? (reverse '(42)) '(42)))
	(assert (equal? (reverse '(1 2 3)) '(3 2 1)))
	(assert (equal? (reverse '(2 3 3)) '(3 3 2)))

	; ------------------
	; <foldr>
	; ------------------
	; Fold to the right.
	; What kind of value it will return depends entirely on
	; the accumulator and the function
	(define foldr (lambda (func acc list)
		(if (null? list)
			acc
			(foldr
				func
				(func acc (car list)) ; acc += item
				(cdr list)
			)
		)
	))

	(assert (equal? (foldr + 0 '(1 2 3)) 6))
	(assert (equal? (foldr cons '() '(1 2 3)) '(1 2 3)))

	; ------------------
	; <foldl>
	; ------------------
	; Fold to the left. See also: foldr
	(define foldl (lambda (func acc list)
		(foldr func acc (reverse list))
	))

	(assert (equal? (foldl + 0 '(1 2 3)) 6))
	(assert (equal? (foldl cons '() '(1 2 3)) '(3 2 1)))
	(assert (equal? (foldl (lambda (acc item) (cons item acc)) '() '(1 2 3)) '(1 2 3)))

	; ------------------
	; <length>
	; ------------------
	; Returns the length of an object.
	(define length (lambda (x)
		(foldr (lambda (acc _) (+ acc 1)) 0 x)
	))

	; ------------------
	; <Map>
	; Given a function `f` transforms (a b c) into ((f a) (f b) (f c)).
	; ------------------

	(define map (lambda (f list)
		(foldr
			(lambda (acc item)
				(cons acc (f item)))
			'()
			list)
	))

	(assert (equal? (map length '((1 2 3) (0 -1 12 3) (3))) '(3 4 1)))
	(assert (equal? (map null? '(() (1) () (2))) '(1 0 1 0)))

	; ------------------
	; <Count>
	; Returns a number of times `item` appears in `list`
	; ------------------

	; foldr-based implementation for lulz
	;(define count (lambda (subject list)
	;	(foldr
	;		(lambda (acc item)
	;			(+ acc (if (equal? subject item) 1 0))
	;		)
	;		0 list)
	;))

	(define count (lambda (item list)
		(if (null? list)
			0
			(+ (equal? item (car list)) (count item (cdr list)))
		)
	))

	(assert (equal? 2 (count 1 '(1 8 7 6 1 9 0))))
	(assert (equal? 3 (count 'foo '(afoo foo bar io foo fooo foo))))

	; ------------------
	; <last>
	; ------------------
	; Returns a list containing last `y` items of `list`.
	; If y >= (length list) then list is original list is returned instead
	(define last (lambda (list y)
		(if (<= (length list) y)
			list
			(last (cdr list) y)
		)
	))

	(assert (equal? (last '(8 7) 5) '(8 7)))
	(assert (equal? (last '(8 7) 2) '(8 7)))
	(assert (equal? (last '(8 7 6 510 31) 3) '(6 510 31)))

	; ------------------
	; <ldiff>
	; ------------------
	(define ldiff (lambda (lhs rhs)
		(if (or (null? lhs) (equal? lhs rhs))
			'()
			(cons (car lhs) (ldiff (cdr lhs) rhs))
		)
	))

	(assert (equal? (ldiff '(3 8 9 1) '()) '(3 8 9 1)))
	(assert (equal? (ldiff '(3 8 9 1) '(1)) '(3 8 9)))
	(assert (equal? (ldiff '(3 8 9 1) '(9 1)) '(3 8)))
	(assert (equal? (ldiff '(3 8 9 1) '(8 9 1)) '(3)))
	(assert (equal? (ldiff '(3 8 9 1) '(9 2)) '(3 8 9 1)))
	(assert (equal? (ldiff '(3 8 9 1) '(0 0)) '(3 8 9 1)))

	; ------------------
	; <apply>
	; ------------------
	(define apply (lambda (func args)
		(foldr func (car args) (cdr args))
	))

	(assert (equal? (apply + '(2 3 4)) 9))
	(assert (equal? (apply cons '((1 2 3) (3) (4))) '(1 2 3 3 4)))

	; ------------------
	; <curry> (two args)
	; ------------------

	; TODO: implement many args curring (recursively?)
	(define curry (lambda (func arg1)
		(lambda (arg2)
			(apply func (cons arg1 arg2))
		)
	))

	(define zero? (lambda (x) ((curry = 0) x)))
	(define positive? (lambda (x) ((curry < 0) x)))
	(define negative? (lambda (x) ((curry > 0) x)))

	(assert (equal? (zero? -1) #f))
	(assert (equal? (zero? 0) #t))
	(assert (equal? (zero? 1) #f))

	(assert (equal? (positive? -1) #f))
	(assert (equal? (positive? 0) #f))
	(assert (equal? (positive? 1) #t))

	(assert (equal? (negative? -1) #t))
	(assert (equal? (negative? 0) #f))
	(assert (equal? (negative? 1) #f))

	; Returns a list containing only add those items from `list`
	; for which (predicate item) equals true.
	; Thus, `predicate` must be a single-argument lambda.
	(define filter (lambda (list predicate)
		(foldr
			(lambda (acc item)
				(if (predicate item) (cons acc item) acc)
			)
			'()
			list
		)
	))

	(assert (equal? '(1 3 5 7) (filter '(1 2 3 4 5 6 7) (lambda (x) (odd? x)))))
	(assert (equal? '() (filter '() null?) ))
	(assert (equal? '() (filter '() (lambda (x) #t))))
	(assert (equal?
			'(foo bar)
			(filter '(foo bar) (lambda (x) #t))
	))
	(assert (equal?
			'()
			(filter '(foo bar) (lambda (x) #f))
	))
)
