(require 'transient)

(defvar aoc/base-dir (expand-file-name "~/Documents/python-stuff/advent-of-code/2024/"))

(defun aoc/open-day (base-dir)
  (interactive (list (read-directory-name "Enter the directory for the day/part you want to work on (must already exist): " aoc/base-dir)))
  (let* ((formatted-base-dir (file-name-as-directory base-dir))
	 (solution-file (concat formatted-base-dir "solution.py"))
	 (test-file (concat formatted-base-dir "test.py"))
	 (test-input-file (concat formatted-base-dir "test-input.txt")))
    (unless (file-exists-p solution-file)
      (error (concat solution-file " does not exist!")))
    (unless (file-exists-p test-file)
      (error (concat test-file " does not exist!")))
    (unless (file-exists-p test-input-file)
      (error (concat test-input-file " does not exist!")))
    (find-file-existing solution-file)
    (delete-other-windows)
    ;; Create a window for the compilation buffer, but don't put anything in it yet. We'll do that
    ;; later on below.
    (split-window-right)
    (other-window 1)
    ;; Test input on bottom right
    (split-window-below)
    (other-window 1)
    (find-file-existing test-input-file)
    ;; Unit test file beside that to the right
    (split-window-right)
    (other-window 1)
    (find-file-existing test-file)
    ;; Go back to the original solution.py file/window that we want to compile
    (other-window 1)
    (compile "make")))

(defun aoc/start-first-part (day-number)
  (interactive "sEnter today's number and I'll create the corresponding directory and template files for the first day's puzzle: ")
  (let* ((source-dir (concat aoc/base-dir "template"))
	 (target-dir (concat aoc/base-dir day-number "/01")))
    (if (file-exists-p target-dir)
	(error (concat "Directory " target-dir " already exists! Exiting without creating anything.")))
    (copy-directory source-dir target-dir nil t t)
    (aoc/open-day target-dir)))

(defun aoc/start-second-part (base-dir)
  (interactive (list (read-directory-name "Enter the day's directory where you've already done part one: " aoc/base-dir)))
  (let ((source-dir (concat base-dir "01/"))
	(target-dir (concat base-dir "02/")))
    (unless (file-exists-p source-dir)
      (error (concat "Could not find directory 01 in " base-dir)))
    (if (file-exists-p target-dir)
	(error (concat "Directory 02 already exists in " base-dir)))
    (copy-directory source-dir target-dir nil t t)
    (aoc/open-day target-dir)))

(transient-define-prefix aoc/commands ()
  :transient-non-suffix 'transient--do-stay
  ["Various shortcuts and automation related to Advent of Code"
   [("o" "Open solution, test input, etc. files for a previously-started day and nicely arrange all the buffers" aoc/open-day)
    ("sf" "Start the first part of day's puzzle. Generate the base files needed, open everything, and arrange buffers" aoc/start-first-part)
    ("ss" "Start the second part of a day's puzzle. Copy the solution to the first part to a new folder, open everything, and arrange buffers" aoc/start-second-part)]])

(provide 'aoc-utils)
