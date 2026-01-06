---
title: Commands
---
**Creating a `Gemfile`:** A `Gemfile` is a manifest that lists all the dependencies for your project. You can create one manually or let Bundler do it for you with the following command. This command will create a new `Gemfile` in your project's root.

```
bundle init
```

**Installing gems with Bundler:** Instead of using `gem install`, you use Bundler's command (this let's you isolate instead of installing globally). If there are issues with packages, remove `Gemfile.lock` and run `bundle install` again.

```
bundle install
```

**Serving:** When you’re developing a site use the following command to serve.

```
jekyll serve
```

To force the browser to refresh with every change use,

```
jekyll serve --livereload
```

**Serving with Bundling:** For bundling use the following command (`--livereload` is optional).

```
bundle exec jekyll serve --livereload --port 4000
```

**Switching to Production:** The most basic way to switch to production is to run a production build using,

```
JEKYLL_ENV = production bundle exec jekyll build
```

By default `JEKYLL_ENV` is development. The `JEKYLL_ENV` is available to you in liquid using `jekyll.environment`. So to only output the analytics script on production you would do the following:

```liquid{% raw %}
{% if jekyll.environment == "production" %}
  <script src="my-analytics-script.js"></script>
{% endif %}
{% endraw %}
```

**Cleaning a site:**

```
bundle exec jekyll clean
```

More info: [Jekyll - Deployment](https://jekyllrb.com/docs/step-by-step/10-deployment/)