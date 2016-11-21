Changelog
=========

1.4.1 (unreleased)
------------------

- Fix i18n domain; update Brazilian Portuguese and Spanish translations.
  [hvelarde]

- Fix package dependencies.
  [hvelarde]


1.4.0 - 2015-12-08
------------------

- update to use z3c.form so it'll work with Plone 5
  [vangheem]

- Added upgrade step to allow control panel icon upgrade to happen without
  reinstalling.
  [davidjb]

- Repository moved to github
  [cewing]

1.3.1 - 2011-10-4
------------------

- Include CMFCore permission on Plone 4.1
  [rich_lewis2]

- Added icon to control panel GS file.
  [ggozad]

1.3 - 2010-09-08
----------------

- Fixed the ``Manage aliases`` form in the controlpanel to include its form
  controls.
  [soerensigfusson, hannosch]

- Removed tabindex to work with Plone 4.
  [stonor]

- Added notification for when a user is managing the aliases of a default item
  in a container instead of the container with a link. Took idea and
  implementation from the @@sharing control panel.
  [dunlapm]

1.3b1 - 2010-07-03
------------------

- Removed all ``*.mo`` files from the locales directory, as these don't need to
  be versioned.
  [WouterVH]

- Added the z3c.autoinclude entry point so this package is automatically loaded
  on Plone 3.3 and above.
  [WouterVH]

- Reorganised \*.txt-files into toplevel-folder or /docs-folder to match current
  best-practices.
  [WouterVH]

- Removed version.txt to avoid deprecation-warning on Zope-startup.
  [WouterVH]

- Changed IRedirectionTool into a Zope 3 interface.
  [davisagli]

- Added Dutch (nl) translation.
  [WouterVH]

- Added basque (eu) translation.
  [erral]

- Regenerated PO files.
  [erral]

- Added bulk upload capability.
  [erikrose]


1.2.1 - 2009-02-11
------------------

- Fixed bugs that caused incorrect display of redirects on the
  @@manage-aliases and @@aliases-controlpanel pages.
  [hexsprite]

- Expanded readme and packaged the release.
  [erikrose]


1.2 - 2007-11-07
----------------

- Updated for Plone 3 by using plone.app.redirector, replacing skin parts
  with a view + template, using GenericSetup for installation and migrate
  existing redirections on install.
  [fschulze]

- Use new permission "RedirectionTool: Modify aliases" for the alias tab.
  [fschulze]

- When adding an alias a security check is performed on the source path.
  This prevents users from linking to their own content from locations to
  which they normally don't have access.
  [fschulze]

Prior 1.2
---------

- Take into account site property allowAnonymousViewAbout in not_found_message

- Added german translation.
  [spamsch]

- Added default validators and actions.
  [spamsch]

- Moved ActionProviderBase before SimpleItem so that actions tab is shown in ZMI
