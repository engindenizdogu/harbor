---
title: Quickstart
---
1- Install all [prerequisites](https://jekyllrb.com/docs/installation/).
2- Install the jekyll and bundler [gems](https://jekyllrb.com/docs/ruby-101/#gems) (to avoid installing globally see [[Gem Isolation]]) 

```
gem install jekyll bundler
```

3- Create a new Jekyll site at `./myblog`.

```
jekyll new myblog
```

4- Change into your new directory.

```
cd myblog
```

5- Build the site and make it available on a local server.

```
bundle exec jekyll serve
```

6- Browse to your local host (http://localhost:4000/)
