class Constant:
    ACTION_MY_STORE_COURSES_UPDATE = "cn.ulearning.yxy.action.mystorecourseupdate"
    ACTION_SYNC_COURSE = "cn.ulearning.yxy.action.sync_course"
    AGREEMENT_KEY = "user_agreement_key"
    CACHE_FILE_LIMIT_TIME = 1209600000
    CORDOVA_FILE = "cdvfile://umooc_cordova"
    COURSE_APP_ASSESS = "course_app_assess"
    COURSE_APP_CLASS = "course_app_class"
    COURSE_APP_DISCUSS = "course_app_discuss"
    COURSE_APP_EXAM = "course_app_exam"
    COURSE_APP_LIVE = "course_app_live"
    COURSE_APP_MEMBER = "course_app_member"
    COURSE_APP_RESOURCE = "course_app_resource"
    COURSE_APP_SPOKEN = "course_app_spoken"
    COURSE_APP_TEXTBOOK = "course_app_textbook"
    COURSE_APP_UNITS = "course_app_units"
    COURSE_APP_WORDS = "course_app_words"
    COURSE_APP_WORK = "course_app_work"
    COURSE_LEARN_IMAGE_ACTIVITY_IMAGE_STRING = "CourseLearnImageActivityImageString"
    DEFAULT_EXPIRY_TIME = 60000
    DEFAULT_PWD = "ulearning"
    ERROR = "error"
    FILE_PATH = "filepath"
    GENERIC_ACTIVITY_COURSE_LESSON_POSITION_INT = "GenericActivityCourseLessonPositionInt"
    GENERIC_ACTIVITY_COURSE_LESSON_SECTION_PAGE_POSITION_INT = "GENERIC_ACTIVITY_COURSE_LESSON_SECTION_PAGE_POSITION_INT"
    GENERIC_ACTIVITY_COURSE_LESSON_SECTION_POSITION_INT = "GenericActivityCourseLessonSectionPositionInt"
    PAGESIZE = 20
    POST_FAIL = "fail"
    RECORD_AUDIO_SIZE = 300
    RECORD_MSG_SIZE = 60000
    REQUEST_ACTIVE_TEXTBOOK = 13
    REQUEST_MODIFY_COURSE = 14
    REQUEST_PERMISSION_AUDIO = 12
    REQUEST_PERMISSION_CAMERA = 11
    REQUEST_PERMISSION_EXTERNAL = 13
    REQUEST_PERMISSION_READ_PHONE_STATE = 14
    STATUS_KEY = "status"
    SUCCESS = "success"
    TEXTSIZE = 500
    TIMESTAMP = "timestamp"
    TWO_DAY = 10368000

    class DOWNLOAD:
        ERROR = 0
        FINISH = 1
        NORMAL = -1
        PAUSE = 3
        PROCESS = 2

    class HANLDER_WHAT:
        FAIL = 0
        SUCCESS = 1

    class RegString:
        FILL_REG = r":|!|\.|\"|\(|\)|\*|\+|,|-|<|>|=|\?|\[|\]|\^|_|{|}|~|`|\s|‘|’|。|“|”|，|＇|，|。|？|！|：|、|@|……|“|”|；|‘|’|～|\.|-|（|）|《|》|〈|〉|〔|〕|\*|\\&|\［|\］|【|】|——|｀|#|￥|\%|ˇ|•|\+|=|\｛|\｝|ˉ|¨|．|｜|〃|\‖|々|「|」|『|』|〖|〗|∶|＇|＂|／|＊|＆|＼|＃|＄|％|︿|＿|＋|－|＝|＜| |'|\p{Blank}"

    class STATUS:
        ALL = 0
        DISABLED = 2
        PROGRESS = 1
