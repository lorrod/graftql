from examples.tutorial.business_logic.permissions import IsItemOwnerOrAdmin


class IsStudentCourse(IsItemOwnerOrAdmin):
    item_id_field = "course_id"
    owner_relation_field = "students"
