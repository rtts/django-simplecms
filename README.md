# SimpleCMS

**This is the simple, Django-based CMS used by
  [Return to the Source](https://rtts.eu/), provided here for everyone
  to use under the [GPLv3](LICENSE) license as part of our free and
  open source philosophy. Also check out our [other
  projects](https://github.com/rtts)!**

## Getting started

SimpleCMS provides everything to create websites that can be edited by
end users. Here's how to start a new project:

    $ pip install django-simplecms
    $ simplecms my_awesome_website

This will create a new directory containing a fully configured Django
project with models, views and templates. It is a renamed copy of the
included [example](example) project.

## Architecture

SimpleCMS has a rather unique take on Django's MVT architecture.
Contrary to regular Django websites, it allows you to write a Django
view for each *section*, rather than for each *page* on your website.
On which pages these sections appear, and in which order, is left to
the content editors rather than the programmer. The included edit
interface lets them assign sections to pages and fill sections with
content.

Here's an example `views.py` of an app using SimpleCMS:

```python
from cms.views import SectionView
from cms.decorators import section_view

@section_view
class HelloWorld(SectionView):
    verbose_name = 'Hello world section'
    fields = ['content']
    template_name = 'hello.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Hello World!'
        return context
```

And here is the contents of `hello.html`:

```html
<section>
    <h1>{{ message }}</h1>
    {{ section.content }}
</section>
```

This means that end users can supply the content for each section, and
programmers can optionally supply additional logic for each section.
Every time a section needs to be rendered, SimpleCMS will call the
appropriate section view and insert the rendered result into the final
rendered page.

## The edit interface

Somewhat like the Django Admin site, SimpleCMS comes with its own
editing environment, albeit much simpler and only suitable for editing
pages and sections. After authenticating, you can click the "edit"
button on any page of the website to alter, add or rearrange sections.

For each section, the section type can be selected from a dropdown
menu. As you can see in `views.py` above, each section type comes with
its own list of editable fields. Client-side JS will hide/show the
relevant fields based on the selected section type. All sections are
stored in the same database table.

## Batteries included!

SimpleCMS includes a variety of useful template tags, middlewares,
reusable views and models, and all the other boilerplate code needed
for new projects.

## Feedback

We love to hear from you! Feel free to [open an
issue](https://github.com/rtts/django-simplecms) or fill out the
contact form on [our website](https://rtts.eu/) (which is of course
built with SimpleCMS!)
