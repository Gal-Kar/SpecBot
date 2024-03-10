from typing import Final

CHILD_SQS: Final[str] = 'child-crawler'
CHILD_SQS_RESULT: Final[str] = 'child-crawler-result'
CHILD_BUCKET: Final[str] = 'child-crw'
CHILD_DATA_FILENAME: Final[str] = 'child-data.json'

PARENT_SQS: Final[str] = 'parent-crawler'
PARENT_SQS_RESULT: Final[str] = 'parent-crawler-result'
PARENT_BUCKET: Final[str] = 'parent-crw'
PARENT_DATA_FILENAME: Final[str] = 'crawler-data.json'

BRUTE_SQS: Final[str] = 'brute-crawler'
BRUTE_SQS_RESULT: Final[str] = 'brute-crawler-result'
BRUTE_BUCKET: Final[str] = 'brute-crw'
BRUTE_DATA_FILENAME: Final[str] = 'brute-data.json'

VULNERABILITY_SCANNER_SQS: Final[str] = 'vulnerability-scanner'
VULNERABILITY_SCANNER_SQS_RESULT: Final[str] = 'vulnerability-scanner-result'
VULNERABILITY_SCANNER_BUCKET: Final[str] = 'vulnerability-scn'
VULNERABILITY_SCANNER_FILENAME: Final[str] = 'vulnerability-scanner-data.json'

JS_SYNTAX_CHECKER_SQS: Final[str] = 'js-syntax-checker'
JS_SYNTAX_CHECKER_SQS_RESULT: Final[str] = 'js-syntax-checker-result'
JS_SYNTAX_CHECKER_BUCKET: Final[str] = 'js-syntax-checker' 
JS_SYNTAX_CHECKER_DATA_FILENAME: Final[str] = 'js-syntax-checker-result.json'

HTML_VALIDATOR_SQS: Final[str] = 'html-validator'
HTML_VALIDATOR_SQS_RESULT: Final[str] = 'html-validator-result'
HTML_VALIDATOR_BUCKET: Final[str] = 'html-validator' 
HTML_VALIDATOR_DATA_FILENAME: Final[str] = 'html-validator-result.json'

ERROR_SCANNER_SQS: Final[str] = 'error-scanner'
ERROR_SCANNER_SQS_RESULT: Final[str] = 'error-scanner-result'
ERROR_SCANNER_BUCKET: Final[str] = 'error-scanner' 
ERROR_SCANNER_DATA_FILENAME: Final[str] = 'error-scanner-result.json'