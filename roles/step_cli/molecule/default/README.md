# step_cli molecule tests

To run these tests locally, follow these steps:

1. Install docker and make sure the current user can access it
2. Install requirements.txt with pip: `pip3 install -r requirements.txt`
3. Install the testing galaxy dependencies: `ansible-galaxy collection install -r requirements.yml`
4. Make sure that you don't have a version of `maxhoesel.smallstep` installed. Molecule might
   be unable to include the correct roles if you do.

You can now run the tests using `molecule test` from the *main role directory*.