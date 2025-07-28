# Checklist for releasing Python WireMock

- [ ] Bump version number
- [ ] Publish the release note
- [ ] Announce on the WireMock Community Slack
- [ ] Announce on social

## Pre-release - bump version number
Make sure the version number has been updated. Do this by updating the version in `./pyproject.toml`:

```toml
[tool.poetry]
name = "wiremock"
version = "2.7.0"
```

Commit and push the changes made.

## Publish the release note
Release drafter should have created a draft release note called "next". Check it for sanity and edit it to add any 
additional information and then set the tag to the version you have just added above.  You can then publish the release.

Publishing the release should trigger the release action to publish to PyPI

## Post an announcement on the WireMock Community Slack
Announce in the #announcments channel then link to the message from #general.

## Shout about it on as many social media platforms as possible
You know the drill.