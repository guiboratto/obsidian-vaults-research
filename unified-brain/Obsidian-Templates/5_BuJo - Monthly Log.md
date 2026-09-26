---
tags:
  - type/structure
  - structure/bujo
created: {{DATE:YYYY-MM-DD, HH:mm}}
modified: {{DATE:YYYY-MM-DD, HH:mm}}
template_type: BuJo Monthly
template_version: "1.20"
---
<!--  See "Template Help" below for using properties -->

# {{Title}}

<!-- Main STRUCTURE of my content -->
[Monthly Logs 2025](Monthly%20Logs%202025.md) | [[2025]]
___

### OKRs*
<!-- DataView table, use example and modify -->

```dataview
TABLE WITHOUT ID
	file.link as "<small>[OKRs](OKRs%202023.md)</small>",
	template_type as "<small>Element</small>"
WHERE status = "active_2025"
SORT file.name DESC
```
<small>*) Objectives (3-4) & Key Results (1-4)</small>

### Kanban

```dataview
TABLE WITHOUT ID
	file.link AS "<small>3_Doing - [Kanban](Kanban%20Board.md)</small>",
	length(file.tasks) AS "<small>Tasks"
WHERE kanban = "doing" 
SORT file.ctime ASCENDING
```

### Tasks

___

### Calendar
.01
.02 
.03
.04
.05
.06
.07
.08
.09
.10
.11
.12
.13
.14
.15
.16
.17
.18 
.19
.20
.21
.22
.23
.24
.25
.26 
.27
.28
.29
.30
.31

---

---
# Back Matter

**_Sources_**
<!-- always keep a link to the [[source]] --> 
- based_on::

**_References_**
<!-- see: [[permanent note]] because <reason> -->
- see:: 

**_Context_**
<!-- the scene at capture — see Subjective Context Principle. Optional but preferred. -->
- scene:: 

**_Terms_**
<!-- optional link to [[literature note]] with term & definition. -->
- term::

**_Targets_**
<!-- optional link to [[project note]] or published content. -->
- used_in::

**_Template Help_**
<!-- link to external help pages on GitHub. -->
- [GitHub - Obsidian-Templates for Zettelkasten.](https://github.com/groepl/Obsidian-Templates)

<!--  © 2022-2026 by Edmund Gröpl under CC BY-NC-SA 4.0 -->
