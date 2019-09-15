# How to contribute

This project is intended to be open to all and a true community effort. Everyone should feel empowered to contribute additional photos, blogs, talks, papers, research, etc for individuals listed. 

## Contributors

Contributors are the public community members who do not have specific access to the RestInCode repository. This would be the majority of people who want to help contribute.

### Adding a new person

Submit an [Issue](https://github.com/restincode/restincode/issues) with the following content:

 * Title: FIRSTNAME LASTNAME (HANDLE)
 * Body: Please provide as much or as little information as you have about the individual.
 * Content suggestions: Contributions (software, hardware, research), Publications (Books, Blogs, Talks), Social Media (Twitter, about.me, mastodon), Wiki pages, LinkedIn, and an Obituary

You can also choose to submit the json file (located in [people/](https://github.com/restincode/restincode/tree/master/people)) directly and fill out as much information as you can. Alternatively you can have us do it for you by just opening an Issue. If you wish to submit your own json, please utilize this [template](https://github.com/restincode/restincode/blob/master/people/_template.json) to get started.

### Adding new data to a person

If there is an existing [Issue](https://github.com/restincode/restincode/issues) for the person, utilize that Issue to suggest additional content from the "Content Suggestions" above. Please do not create new tickets for People that already exist. Any new contributions or discussion about an individual should go in a single Issue for that person.

Alternatively, submit a Pull Request with the changes to the individuals json file, and we will review it.

## Maintainers

Maintainers are the people who have commit access to the RestInCode repository and can manage Issues and Pull Requests.

### Triaging a new Issue

The majority of new GitHub Issues will be used to add new individuals to Rest In Code (RiC). The Issue subject will be a real name and/or a handle. **An open Issue to add a person should never be closed**. It will be used long-term to add new data and discuss the current memorial of this individual. Anyone is welcome to contribute, including sharing links related to the person, personal stories, or general thoughts on their friends who have passed. Use labels to identify what work if any needs to be completed on the current Issue/person.

#### What to look for

Verify there are no duplicate Issues for this name or handle. If there are, attempt to merge their contents and apply appropriate labels.

#### Using Labels

* **Add Person** - If this is a new person who doesn't exist in people/, apply this label to identify the need for them to be added. This should be removed after the person has been successfully added to RiC.
* **Add Data** - If this is new data for an existing person, this label should be applied to the existing Issue for that person. This should be removed once the new data has been added to the person in RiC.
* **People** - This is a pemament label that will always be applied and never removed from an Issue that represents a person.
* **Person Added** - This label should be applied after the person has been added to people/. The issue should remain Open for additional changes, but this label represents that the individual has been added to RiC.

### Triaging a Pull Request

Pull requests could be anything from People, new data, code changes, web site changes, documentation or more. Applying the appropriate labels will be most important to ensuring they are handled correctly.

#### What to look for

The big thing to look for will be that the persons name is spelled correctly in all places (people/<name>.json, inside the name.json, in the peoplelist.json, images/<name>.(jpg|png), etc). This name should match in all places. Verify any social media links, references, or other URLs that may wind up on the final memorial are working and go where expected.

#### Using Labels

* **Add Person** - This shows that the PR is to add a new person to the RiC project.
* **Add Data** - This shows that the PR is to add additional data, such as contributions or images to an existing person.
* **BUG** - A bug in the actual website/github config/or jsons.
* **Code** - A change to the actual code for this website.
* **Ideas** - A proposed idea or change to the project, website, templates, or other materials.
* **Needs Review** - This PR requires a Maintainer to review the changes and ensure that everything looks appropriate and up to standards.
* **People** - This represents an Issue or PR that is specifically about a person in the memorial.
* **Person Added** - This represents a person who's been added (a json created) to the memorial. Should be applied after the work is complete, and should replace the "Add Person" tag.
* **Project** - Used to identify issues or PRs that relate to the RiC project and not any of the people within it.
* **Task** - A basic task being requested. This could fall within project, code, bug, or other non people focussed work.
* **Work in Progress** - This will be applied if the pull request (PR) should **NOT** be accepted in its current state. This is for work-in progress PR's that require more work from the contributor.
