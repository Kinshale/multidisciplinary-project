# Bluesky Event Types

## Core Social Actions

### Following
- `('create', 'app.bsky.graph.follow')` - Follow a user
- `('delete', 'app.bsky.graph.follow')` - Unfollow a user

### Engagement
- `('create', 'app.bsky.feed.like')` - Like a post
- `('delete', 'app.bsky.feed.like')` - Remove a like

### Posts
- `('create', 'app.bsky.feed.post')` - Create a post
- `('update', 'app.bsky.feed.post')` - Update a post
- `('delete', 'app.bsky.feed.post')` - Delete a post

### Reposts
- `('create', 'app.bsky.feed.repost')` - Create a repost
- `('delete', 'app.bsky.feed.repost')` - Delete a repost

## User Management

### Profiles
- `('create', 'app.bsky.actor.profile')` - Create user profile
- `('update', 'app.bsky.actor.profile')` - Update user profile

### Blocking
- `('create', 'app.bsky.graph.block')` - Block a user
- `('delete', 'app.bsky.graph.block')` - Unblock a user

- `('create', 'app.bsky.graph.listblock')` - Create a block list
- `('delete', 'app.bsky.graph.listblock')` - Delete a block list

## Content Organization

### Lists
- `('create', 'app.bsky.graph.list')` - Create a list
- `('update', 'app.bsky.graph.list')` - Update a list
- `('delete', 'app.bsky.graph.list')` - Delete a list

- `('create', 'app.bsky.graph.listitem')` - Add user to list
- `('delete', 'app.bsky.graph.listitem')` - Remove user from list

### Starter Packs
- `('create', 'app.bsky.graph.starterpack')` - Create starter pack
- `('update', 'app.bsky.graph.starterpack')` - Update starter pack
- `('delete', 'app.bsky.graph.starterpack')` - Delete starter pack

*Starter packs are collections of accounts, lists, and feeds that help users discover interesting content or communities.*

## Content Moderation

### Post Gates
- `('create', 'app.bsky.feed.postgate')` - Add post restrictions
- `('update', 'app.bsky.feed.postgate')` - Modify post restrictions
- `('delete', 'app.bsky.feed.postgate')` - Remove post restrictions

*Restricts actions like commenting and replying on specific posts.*

### Thread Gates
- `('create', 'app.bsky.feed.threadgate')` - Add thread restrictions
- `('update', 'app.bsky.feed.threadgate')` - Modify thread restrictions
- `('delete', 'app.bsky.feed.threadgate')` - Remove thread restrictions
*Restricts actions on threads (series of connected posts).*

## Custom Feeds & Scheduling

### Feed Generators
- `('create', 'app.bsky.feed.generator')` - Create custom feed
- `('update', 'app.bsky.feed.generator')` - Update custom feed
- `('delete', 'app.bsky.feed.generator')` - Delete custom feed

*Custom feeds are typically created on third-party websites.*

### Scheduled Posts
- `('create', 'app.vercel.schedulesky')` - Schedule a post
- `('delete', 'app.vercel.schedulesky')` - Delete scheduled post

*Third-party scheduling functionality.*

## Other Events
The following event types have unknown or unspecified functionality:

- `('update', 'app.bsky.labeler.service')`
- `('create', 'blue.badge.collection')`
- `('create', 'chat.bsky.actor.declaration')`
- `('update', 'chat.bsky.actor.declaration')`
- `('create', 'fyi.unravel.frontpage.post')`
- `('create', 'fyi.unravel.frontpage.vote')`
- `('create', 'events.smokesignal.app.profile')`
- `('update', 'events.smokesignal.calendar.rsvp')`
- `('create', 'com.whtwnd.blog.entry')`
- `('update', 'com.whtwnd.blog.entry')`
- `('create', 'com.example.status')`
- `('update', 'com.example.status')`
- `('create', 'app.tighttesx.feed.post')`