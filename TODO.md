# Automat TODO list

## TODO

Here is the list of changes to test/implement:

* HTTP APIs to:
  - Add a project                              [DONE]
  - Update a project                           [DONE]
  - Remove a project                           [DONE]
  - Build a project                            [DONE]
* Environment variables
  - Step-level                                 [DONE] 
  - Project-level                              [DONE]
  - Database-level                             [TODO]
* Error handling during checkout               [DONE]
* Error handling during build                  [DONE]
* Store build record                           [TODO]
* No build if no changes                       [TODO]
* Store build artifacts                        [TODO]
* Replay a build                               [TODO]
* Live monitoring of project files             [TODO]
* Asynchronous build                           [TODO]
* Periodic scheduling of build                 [TODO]
* E-mail notification (basic)                  [TODO]
* Compute the list of changes between builds   [TODO]

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
