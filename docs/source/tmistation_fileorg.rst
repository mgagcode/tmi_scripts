File Organization
#################

Naming and organizing the location of files is a difficult thing to prescribe because your needs
may require a specific solution.  Regardless, a general proposal will be given and from there one can
create a more specific solution.

The proposed general purpose solution assumes that version control is an important issue for you.

Consider the following scenario.  A product is in full production and there is a test that is having a 1% failure
rate, but none of the customer returns are associated with failures for this test.  So an ECO is created to change the
limit of the test to reduce the failure rate to an expected 0.5%.  How should you implement this change so that you
can track the new failure rate?  Or search if a product returned would have failed at the previous limit?  These
are the kinds of things you need to think about when you implement test program and script files.

TMIStation has a high level prescribed directory structure.

Constraints:

* all TMIStations files must be under ``./public/station``
* all script files must be under ``./public/station/scripts``

Proposal:

::

    ./public/station/scripts/companyName
    ./public/station/scripts/companyName/product1
    ./public/station/scripts/companyName/product1/p1_stage1_v1.tmiscr
    ./public/station/scripts/companyName/product1/p1_stage2_v1.tmiscr
    ./public/station/scripts/companyName/product1/p1_stage2_v2.tmiscr
    ./public/station/scripts/companyName/product1/p1_testsA_v1.py
    ./public/station/scripts/companyName/product1/p1_testsB_v1.py
    ./public/station/scripts/companyName/product1/p1_testsB_v2.py
    ./public/station/scripts/companyName/product1/p1_testsC_v1.py
    ./public/station/scripts/companyName/product1/p1_testsD_v1.py
    ./public/station/scripts/companyName/product2
    ./public/station/scripts/companyName/product2/p2_stage1_v1.tmiscr
    ./public/station/scripts/companyName/product2/p2_stage2_v1.tmiscr
    ./public/station/scripts/companyName/product2/p2_testsA_v1.py
    ./public/station/scripts/companyName/product2/p2_testsB_v1.py
    ./public/station/scripts/companyName/product2/p2_testsC_v1.py
    ./public/station/scripts/companyName/product2/p2_testsD_v1.py
    ./public/station/scripts/companyName/comm_code
    ./public/station/scripts/companyName/comm_code/comm_codeA.py
    ./public/station/scripts/companyName/comm_code/comm_codeB.py

* create a path for each different type/class/model of product
* what causes a product to be different from another product (product1 vs product2) is up to you
* its assumed that a product may be tested in stages, so there will be a script file for each stage
* every file has a version number
* more than one version of a file may be in use at one time

  * for example, if two models of the product and in production at the same time, and use different scripts, then
    both scripts need to be available

* There might be some common code that can be used across products
* there should not be a file with the same name anywhere in the directory structure
* for development work, you may create a product directory that reads ``dev_product3`` and in this way
  separate engineering files from production files
