# Automat TODO list

## TODO

Here is the list of changes to test/implement:

* HTTP APIs to:
  - Add a project                              [DONE]
  - Update a project                           [DONE]
  - Remove a project                           [DONE]
  - Build a project                            [DONE]
* Environment variables
  - Step-level                                 [TODO] 
  - Project-level                              [TODO]
  - Database-level                             [TODO]
* Error handling during checkout               [TODO]
* Error handling during build                  [TODO]
* Store build record                           [TODO]
* No build if no changes                       [TODO]
* Store build artifacts
* Replay a build
* Live monitoring of project files
* Asynchronous build
* Periodic scheduling of build
* E-mail notification (basic)
* Compute the list of changes between two builds

## Wish List

Here is a list of features that are not scheduled yet:

* Event listening with WebSockets
* E-mail customization with templates
* Web interface customization using templates
* Live monitoring of template definitions
* Client authentication
* HTTPS support
* Security review
  - URL name checking
  - Authentication
  - Anonymous access
