Django Simple CMS
=================

Hello stranger! You have stumbled on my personal Django boilerplate
repository. It contains all those code fragments that I find myself
writing over and over again when I create websites for clients.
There's models for Pages and Sections in the `cms` app, as well as
some basic HTML and CSS designs. There's a NumberedModel in the
`numberedmodel` app. There's simple SASS compiler in `simplesass`.

With these apps it's very simple to setup a basic website. Simply use
the project template from the `examples` directory as a starting
point. Then run the following Django commands:

    $ ./manage.py migrate
    $ ./manage.py createsuperuser
    $ ./manage.py runserver --nostatic

(The `--nostatic` argument is needed to make `simplesass` work.)

Now point your browser to http://localhost:8000/ and there will be a
website ready to be edited using the CMS views! All you need to do
next is to hire a graphic designer ;-)
