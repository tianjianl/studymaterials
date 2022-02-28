echo 'all lines that contain a phone number with an extension (the letter x or X followed by four digits).'
echo 'grep '[x,X][0-9]\{4\}' grepdata.txt'
grep '[x,X][0-9]\{4\}' grepdata.txt


echo '---------------------------------'
echo 'all lines that begin with three digits followed by a blank. Your answer must use the \{ and \} repetition specifier'


echo 'grep '^[0-9]\{3\}[[:blank:]]' grepdata.txt'
grep '^[0-9]\{3\}[[:blank:]]' grepdata.txt

echo '---------------------------------'
echo 'all lines that contains a date'
echo 'grep '[A-Z,a-z]\{3\}.[[:blank:]][0-9]\{2\},[[:blank:]]20[0-9]\{2\}' grepdata.txt'
grep '[A-Z,a-z]\{3\}.[[:blank:]][0-9]\{2\},[[:blank:]]20[0-9]\{2\}' grepdata.txt



echo '---------------------------------'
echo 'all lines containing a vowel (a, e, i, o, or u) followed by a single character followed by the same vowel again. Thus, it will find “eve” or “adam” but not “vera"' 
echo 'grep '\([aeiou]\)[a-zA-Z]\1' grepdata.txt'
grep '\([aeiou]\)[a-zA-Z]\1' grepdata.txt



echo '---------------------------------'
echo 'all lines that do not begin with a capital S'
echo 'grep '^[^S]' grepdata.txt'
grep '^[^S]' grepdata.txt


echo '---------------------------------'
echo 'Print all lines that contain CA in either uppercase or lowercase.' 
echo 'grep -i 'CA' grepdata.txt'
grep -i 'CA' grepdata.txt


echo '---------------------------------'
echo 'Print all lines that contain an email address (they have an @ in them), preceded by the line number.'
echo 'grep -n '@' grepdata.txt'
grep -n '@' grepdata.txt


echo '---------------------------------'
echo 'Print all lines that do not contain the word Sep. (including the period).'
echo 'grep -v 'Sep.' grepdata.txt'
grep -v 'Sep.' grepdata.txt


echo '---------------------------------'
echo 'Print all lines that contain the word de as a whole word.'
echo 'grep -w 'de' grepdata.txt'
grep -w 'de' grepdata.txt

