from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Role,Privilege,RolePrivilegeChange,get_current_user,IpaPracticeChange,IPA,Practice
from django.utils import timezone



@receiver(m2m_changed, sender=Role.privileges.through)

def Role_Privilege_changed(sender, instance, action, reverse, model, pk_set, **kwargs):

    if action in ['post_add', 'post_remove']:

        added = action == 'post_add'

        user_who_made_the_change = get_current_user()

        for privilege_id in pk_set:

            privilege = Privilege.objects.get(pk=privilege_id)

            RolePrivilegeChange.objects.create(

                user=user_who_made_the_change,

                role=instance,

                privilege=privilege,

                added=added,

                modified_by=user_who_made_the_change,

                modified_at=timezone.now(),

            )


@receiver(m2m_changed, sender=IPA.practices.through)

def Ipa_Practice_changed(sender, instance, action, reverse, model, pk_set, **kwargs):

    if action in ['post_add', 'post_remove']:

        added = action == 'post_add'

        user_who_made_the_change = get_current_user()

        for practice_id in pk_set:

            practice = Practice.objects.get(pk=practice_id)

            IpaPracticeChange.objects.create(

                user=user_who_made_the_change,

                ipa=instance,

                practice=practice,

                added=added,

                modified_by=user_who_made_the_change,

                modified_at=timezone.now(),

            )