=======================
Custom Statement Models
=======================

ChatterBot allows you to replace the default Statement and Tag models with custom versions,
using a pattern similar to Django's ``AUTH_USER_MODEL`` setting. This enables you to add
custom fields, business logic, and integrations specific to your application.

Why Use Custom Models?
========================

Custom models allow you to:

- **Add custom fields** - User ratings, sentiment scores, metadata, timestamps
- **Implement business logic** - Custom validation, automated tagging, calculations
- **Integrate with existing schemas** - Foreign keys to User models, related data
- **Optimize performance** - Custom indexes, database-specific features
- **Track analytics** - Views, feedback, response times

Creating Custom Models
========================

Step 1: Inherit from Abstract Base Classes
------------------------------------------

ChatterBot provides abstract base classes that define the required fields and methods.
Inherit from these to create your custom models:

.. code-block:: python
   :caption: myapp/models.py

   from chatterbot.ext.django_chatterbot.abstract_models import (
       AbstractBaseStatement,
       AbstractBaseTag
   )
   from django.db import models
   from django.contrib.auth import get_user_model

   User = get_user_model()


   class CustomStatement(AbstractBaseStatement):
       """
       Custom Statement model with user feedback tracking.
       """

       # Add your custom fields
       upvotes = models.IntegerField(default=0)
       downvotes = models.IntegerField(default=0)
       sentiment_score = models.FloatField(null=True, blank=True)
       metadata = models.JSONField(default=dict, blank=True)

       # Track which users interacted
       upvoted_by = models.ManyToManyField(
           User,
           related_name='upvoted_statements',
           blank=True
       )

       # Required: ManyToMany relationship to a Tag model
       # (Can be a custom Tag model or the default)
       tags = models.ManyToManyField(
           'CustomTag',
           related_name='statements',
           blank=True
       )

       class Meta:
           swappable = 'CHATTERBOT_STATEMENT_MODEL'
           indexes = [
               models.Index(fields=['upvotes']),
               models.Index(fields=['sentiment_score']),
           ]

       # Custom properties and methods
       @property
       def score(self):
           """
           Calculate net score.
           """
           return self.upvotes - self.downvotes

       def upvote(self, user):
           """
           Record an upvote from a user.
           """
           if not self.upvoted_by.filter(pk=user.pk).exists():
               self.upvoted_by.add(user)
               self.upvotes += 1
               self.save()


   class CustomTag(AbstractBaseTag):
       """
       Custom Tag model with categorization.
       """

       # Add your custom fields
       category = models.CharField(max_length=64, blank=True)
       is_active = models.BooleanField(default=True)
       priority = models.IntegerField(default=0)

       class Meta:
           swappable = 'CHATTERBOT_TAG_MODEL'
           ordering = ['-priority', 'name']

Step 2: Configure Django Settings
----------------------------------

Tell ChatterBot to use your custom models by adding these settings:

.. code-block:: python
   :caption: settings.py

   # Swappable model configuration (like AUTH_USER_MODEL)
   CHATTERBOT_STATEMENT_MODEL = 'myapp.CustomStatement'
   CHATTERBOT_TAG_MODEL = 'myapp.CustomTag'

   # Standard ChatterBot configuration
   CHATTERBOT = {
       'name': 'My Bot',
       'storage_adapter': 'chatterbot.storage.DjangoStorageAdapter',
       'logic_adapters': [
           'chatterbot.logic.BestMatch',
       ]
   }

   # Add your app to INSTALLED_APPS
   INSTALLED_APPS = [
       # ... other apps
       'django_chatterbot',  # ChatterBot's Django app
       'myapp',  # Your app with custom models
   ]

Step 3: Create and Run Migrations
----------------------------------

Generate and apply migrations for your custom models:

.. code-block:: bash

   # Create migrations for your custom models
   python manage.py makemigrations myapp

   # Apply migrations
   python manage.py migrate

ChatterBot will now use your custom models automatically.

Required Fields and Methods
============================

Your custom Statement model **must include**:

Required Fields (from AbstractBaseStatement)
---------------------------------------------

- ``text`` - The statement text (CharField, max_length from constants)
- ``search_text`` - Indexed search text (CharField)
- ``conversation`` - Conversation identifier (CharField)
- ``created_at`` - Timestamp (DateTimeField)
- ``in_response_to`` - Previous statement text (CharField, nullable)
- ``search_in_response_to`` - Indexed previous text (CharField)
- ``persona`` - Speaker identifier (CharField)
- ``tags`` - ManyToManyField to your Tag model

Required Methods
----------------

- ``get_tags()`` - Returns list of tag name strings
- ``add_tags(*tags)`` - Adds tags to the statement
- ``__str__()`` - String representation (inherited from abstract base)

Your custom Tag model **must include**:

Required Fields (from AbstractBaseTag)
--------------------------------------

- ``name`` - Unique tag name (SlugField, unique=True)

Alternative: Per-Instance Configuration
=======================================

You can also specify custom models per ChatBot instance without changing Django settings.
This is useful when running multiple bots with different schemas:

.. code-block:: python
   :caption: views.py

   from chatterbot import ChatBot

   # Bot with custom models
   custom_bot = ChatBot(
       'Custom Bot',
       storage_adapter='chatterbot.storage.DjangoStorageAdapter',
       statement_model='myapp.CustomStatement',
       tag_model='myapp.CustomTag'
   )

   # Bot with default models
   default_bot = ChatBot(
       'Default Bot',
       storage_adapter='chatterbot.storage.DjangoStorageAdapter'
   )

The ``statement_model`` and ``tag_model`` kwargs take precedence over Django settings.

Usage Examples
==============

Example: User Feedback
----------------------

Track user ratings on responses:

.. code-block:: python
   :caption: myapp/models.py

   from chatterbot.ext.django_chatterbot.abstract_models import AbstractBaseStatement
   from django.db import models
   from django.contrib.auth import get_user_model

   User = get_user_model()

   class FeedbackStatement(AbstractBaseStatement):
       """
       Statement with user feedback.
       """

       helpful_count = models.IntegerField(default=0)
       not_helpful_count = models.IntegerField(default=0)

       rated_by = models.ManyToManyField(
           User,
           through='StatementRating',
           related_name='rated_statements'
       )

       tags = models.ManyToManyField(
           'Tag',
           related_name='statements'
       )

       class Meta:
           swappable = 'CHATTERBOT_STATEMENT_MODEL'

   class StatementRating(models.Model):
       """
       Track individual user ratings.
       """
       user = models.ForeignKey(User, on_delete=models.CASCADE)
       statement = models.ForeignKey(FeedbackStatement, on_delete=models.CASCADE)
       is_helpful = models.BooleanField()
       created_at = models.DateTimeField(auto_now_add=True)

       class Meta:
           unique_together = ('user', 'statement')

.. code-block:: python
   :caption: myapp/views.py

   from django.http import JsonResponse
   from django.views.decorators.http import require_POST
   from django.contrib.auth.decorators import login_required
   from myapp.models import FeedbackStatement, StatementRating

   @login_required
   @require_POST
   def rate_statement(request, statement_id):
       statement = FeedbackStatement.objects.get(pk=statement_id)
       is_helpful = request.POST.get('helpful') == 'true'

       rating, created = StatementRating.objects.update_or_create(
           user=request.user,
           statement=statement,
           defaults={'is_helpful': is_helpful}
       )

       # Update counts
       statement.helpful_count = statement.rated_by.filter(
           statementrating__is_helpful=True
       ).count()
       statement.not_helpful_count = statement.rated_by.filter(
           statementrating__is_helpful=False
       ).count()
       statement.save()

       return JsonResponse({
           'helpful': statement.helpful_count,
           'not_helpful': statement.not_helpful_count
       })

Migrating from Default Models
=============================

If you need to migrate an existing project from default to custom models:

1. Create Custom Models
-----------------------

Create your custom models inheriting from the abstract base classes.

2. Update Settings
------------------

Add ``CHATTERBOT_STATEMENT_MODEL`` and ``CHATTERBOT_TAG_MODEL`` to settings.

3. Create Initial Migration
---------------------------

.. code-block:: bash

   python manage.py makemigrations myapp

4. Create Data Migration
-------------------------

Write a data migration to copy existing data:

.. code-block:: python
   :caption: myapp/migrations/0002_copy_chatterbot_data.py

   from django.db import migrations

   def copy_statements(apps, schema_editor):
       # Get old and new models
       OldStatement = apps.get_model('django_chatterbot', 'Statement')
       NewStatement = apps.get_model('myapp', 'CustomStatement')
       OldTag = apps.get_model('django_chatterbot', 'Tag')

       # Copy all statements
       for old_stmt in OldStatement.objects.all():
           new_stmt = NewStatement.objects.create(
               text=old_stmt.text,
               search_text=old_stmt.search_text,
               conversation=old_stmt.conversation,
               created_at=old_stmt.created_at,
               in_response_to=old_stmt.in_response_to,
               search_in_response_to=old_stmt.search_in_response_to,
               persona=old_stmt.persona,
           )

           # Copy tags
           new_stmt.tags.set(old_stmt.tags.all())

   def reverse_copy(apps, schema_editor):
       # Optionally implement reverse migration
       pass

   class Migration(migrations.Migration):
       dependencies = [
           ('myapp', '0001_initial'),
           ('django_chatterbot', '__latest__'),
       ]

       operations = [
           migrations.RunPython(copy_statements, reverse_copy),
       ]

5. Apply Migrations
-------------------

.. code-block:: bash

   python manage.py migrate myapp

Best Practices
==============

1. **Always inherit from abstract base classes** - This ensures compatibility with ChatterBot's storage adapter.

2. **Set swappable in Meta** - Add ``swappable = 'CHATTERBOT_STATEMENT_MODEL'`` to enable model swapping.

3. **Implement required methods** - ``get_tags()`` and ``add_tags()`` are essential for ChatterBot's operation.

4. **Use indexes wisely** - Add database indexes to fields you'll frequently query or filter on.

5. **Test thoroughly** - Test your custom models with ChatterBot's training and conversation features.

6. **Document your schema** - Clearly document any custom fields and their purposes for future maintainers.

Troubleshooting
===============

Model Not Found Error
---------------------

If you see errors like ``LookupError: No installed app with label 'myapp'``:

- Ensure your app is in ``INSTALLED_APPS``
- Check that migrations have been run
- Verify the model path in settings (format: ``'app_label.ModelName'``)

Tags Relationship Error
-----------------------

If you get errors about the tags relationship:

- Ensure your Statement model has a ``tags`` ManyToManyField
- The field must reference your custom Tag model
- Use ``related_name='statements'``

Migration Conflicts
-------------------

If migrations conflict:

- Run ``python manage.py makemigrations --merge``
- Check migration dependencies
- Ensure ChatterBot is migrated before your custom models

See Also
========

- :doc:`/django/settings` - Django settings reference
- :doc:`/storage/django-storage-adapter` - Django storage adapter documentation
- :doc:`/training` - Training your chatbot
