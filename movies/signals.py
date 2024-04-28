from django.core.signals import request_finished
from django.dispatch import receiver
from django.db.models.signals import post_save
from movies.models import SearchTerm
from movies.tasks import notify_of_new_search_term

@receiver(request_finished)
def signal_receiver(sender, **kwargs):
    print(f"Received signal from {sender}")

@receiver(post_save, sender=SearchTerm, dispatch_uid="search_term_saved")
def search_term_saved(sender, instance, created, **kwargs):
    if created:
        # new SearchTerm was created
        notify_of_new_search_term.delay(instance.term)
        print(f"A new SearchTerm was created: '{instance.term}'")