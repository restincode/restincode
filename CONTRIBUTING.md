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

The majority of new issues will be to add new individuals to RiC. Their subject will be a real name and/or a handle. 

#### What to look for

Verify there are no duplicate Issues for this name or handle. If there are, attempt to merge their contents and apply appropriate labels.

#### Using Labels

* **Add Person** - If this is a new person who doesn't exist in people/, apply this label to identify the need for them to be added. This should be removed after the person has been successfully added to RiC
* **Add Data** - If this is new data for an existing person, this label should be applied to the existing Issue for that person. This should be removed once the new data has been added to the person in RiC
* **People** - This is a pemament label that will always be applied and never removed from an Issue that represents a person
* **Person Added** - This label should be applied after the person has been added to people/. The issue should remain Open for additional changes, but this label represents that the individual has been added to RiC

### Triaging a Pull Request

Pull requests could be anything from People, new data, code changes, web site changes, documentation or more. Applying the appropriate labels will be most important to ensuring they are handled correctly.

#### What to look for

The big thing to look for will be that the persons name is spelled correctly in all places (people/<name>.json, inside the name.json, in the peoplelist.json, images/<name>.(jpg|png), etc). This name should match in all places. Verify any social media links, references, or other URLs that may wind up on the final memorial are working and go where expected.

#### Using Labels

* **Work in Progress** - This should be applied if the pull request should NOT be accepted in its current state. This is for WIP PR's that require more work from the contributor
* **Needs Review** - This PR requires a Maintainer to review the changes and ensure that everything looks appropriate and up to standards
* **Add Person** - This shows that the PR is to add a new person to the RiC project
* **Add Data** - This shows that the PR is to add additional Data, such as contributions, images, etc, to an existing person
