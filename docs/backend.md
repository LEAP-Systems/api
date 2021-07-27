# Backend Design

Proposed solution for databasing capture information for algorithm performance analytics
without sacrificing data integrity. The information processed per capture is anonymized
so it can be crowd sourced. No sensitive data is ever sent through the REST API.
Computationally expensive and heavy processing libraries remain on the server side.

1. Calibration
   1. image aquisition
   2. post to backend (/v1/images/ -d {'calibration': true})
   3. evaluate calibration completion -> pre-ECP
   4. return notification to client on calibration pass/fail
   5. if fail new image aquisition
   8. post to backend (/v1/images/ -d {'calibration': true})
   9. backend applies superposition to first image
   10. evaluate calibration completion (check for n number of apex/box detections)
   11. evaluate ECP engine and save results to db session collection
   12. return to client endpoint to fetch ecp calibration weights file
   13. return to client endpoint to fetch tuned gaussian surface
   14. client tunes ecp to specification using weights file
   15. client gets surface fit
2. Frame reads
   1. image acquisition
   2. subtract the image from the surface fit. (numpy only operations)
   3. compute the bright points
   4. run through trained ecp network
   5. apply spatial codec
   6. read data