---
title: Gem Isolation
---
# The Correct Way to Isolate Gems
To achieve the isolation you're looking for with Jekyll, you should use **Bundler**. Bundler is a gem itself, and it's the standard tool for managing Ruby project dependencies. Here is the workflow:

**1- Install Bundler (globally):** You only need to do this **once** on your machine.

```
gem install bundler
```

(This is the one exception to the "don't install globally" rule, as Bundler is the tool that enables your project-specific environments).

**2- Navigate to your project directory:**

```
cd my-jekyll-site
```

**3- Create a `Gemfile`:** A `Gemfile` is a manifest that lists all the dependencies for your project. You can create one manually or let Bundler do it for you.

```
bundle init
```

This command will create a new `Gemfile` in your project's root.
 
 **4- Add your gems to the `Gemfile`:** Open the `Gemfile` in a text editor and add your dependencies, like Jekyll. It should look something like this:

```
source "https://rubygems.org"

gem "jekyll"
gem "jekyll-feed" # A common plugin for Jekyll
```

**5- Install the gems with Bundler:** Now, instead of using `gem install`, you use Bundler's command.

```
bundle install
```

This command reads your `Gemfile`, finds the correct versions of all the gems and their sub-dependencies, and installs them into a dedicated directory _within your project's root folder_ (usually `vendor/bundle` or a hidden `.bundle` directory). It also creates a `Gemfile.lock` file, which locks the exact versions of all gems for a reproducible build.

**6- Run your Jekyll commands with `bundle exec`:** This is the most important step. When you run `bundle exec jekyll serve`, Bundler ensures that the `jekyll` command being executed is the one from your project's isolated environment, not a globally installed version.

```
bundle exec jekyll serve
```

By following this process, you achieve true isolation. Your Jekyll project has its own set of dependencies, and you can work on another Ruby project with a different version of Jekyll or other gems without any conflicts. You also get a `Gemfile.lock` file that can be committed to version control, guaranteeing that anyone who clones your repository will have the exact same environment as you.