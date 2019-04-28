+++
title = "{{ item.name }}"
description = ""
date = "{{ item.date }}" 
draft = true 
tags = ["thing"]
categories = []
img="{{ item.name }}"
+++
{% if item.doc %}{{ item.doc }}{% endif %}
