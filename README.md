# SimpleCMS

***A super simple but very extensible content management system for
Django websites.***

SimpleCMS provides the reusable Django app `cms` which contains
everything you need to create websites that can be easily edited by
end users.

## How does it work?

Contrary to 'regular' Django websites, SimpleCMS allows you to write a
view for each *section*, rather than for each *page* on your website.
On which pages these sections appear, and in which order, is left to
the content editor rather than the programmer. After authenticating,
the user can use the "Edit" interface to fill the website with various
types of content.

Here's an example `views.py` of an app using SimpleCMS:

    from cms.views import SectionView
    from cms.decorators import section_view

    @section_view
    class HelloWorld(SectionView):
        verbose_name = 'Hello world section'
        fields = ['content']
        template_name = 'hello.html'

        def get_context_data(self, **kwargs):
            context = super()get_context_data(**kwargs)
            context['message'] = 'Hello World!'
            return context

And here is the contents of `hello.html`:

    <section type="helloworld">
      <h1>{{message}}</h1>
      {{section.content}}
    </section>

Everytime a section needs to be rendered, SimpleCMS will call the
appropriate section view and insert the rendered result into the final
rendered page.

But that's not all! SimpleCMS is easily extendable. You can add custom
fields to your Page and Section models. You can even add one-to-many
fields by defining new models with a foreign key to the Section model,
and the Edit interface will automagically show the user nested
formsets to edit the related instances! For a complete example see the
included `example` app.

## The "Edit" Interface

Somewhat like the Django Admin site, SimpleCMS comes with its own
editing environment, albeit much simpler and only suitable for editing
pages and sections. After authenticating, the content editor can click
the "edit" button on any page of the website to alter, add or
rearrange sections.

For each section, the section type can be selected from a dropdown
menu. As you can see in `views.py` above, each section type comes with
its own list of editable fields. Client-side javascript will hide/show
the relevant fields based on the selected section type. All sections
are stored in the same database table.

## Batteries included!

SimpleCMS includes a variety of useful template tags, default *Page*
and *Section* models, and all the other boilerplate code needed for
new projects.

One notable inclusion is the `eval` template tag. It will pass its
argument first through Django's templating system and then through
Markdown, making for instance the following possible. (Disclaimer: use
with caution!)

    Welcome to **{% now 'Y' %}!**

Another useful feature is the automatic compilation of `SCSS` files to
`CSS` files using a custom middleware.

## Installation

Use the provided helper command `simplecms` to quickly setup a new
project:

    $ pip install django-simplecms
    $ simplecms mysite

After the project files have been created, initialize the database and
create a superuser:

    $ cd mysite
    $ sudo su postgres -c "createuser mysite; createdb -O mysite mysite"
    $ ./manage.py makemigrations
    $ ./manage.py migrate
    $ ./manage.py createsuperuser

Finally, run the development server and visit
http://localhost:8000/login/ in your browser to log in!

    $ ./manage.py runserver
