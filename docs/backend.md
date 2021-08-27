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


## Shortcut Methodology (Insecure)
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
   12. return the results of ecp to the client
   13. client applies spatial codec and decodes the packet
   14. Generates APR key and sends to transmitter
2. Frame reads
   1. image acquisition
   2. subtract the image from the surface fit. (numpy only operations)
   3. compute the bright points
   4. run through trained ecp network
   5. apply spatial codec
   6. read data

## Image Processing Endpoints and Queries

`POST /v1/model`
Records modelling input parameters:
```py
{
   "divisor": 2,
   "iterations": 5000,
   "capture_id": "u43o42043247204",
   "processing_id": "eywuiqeuqguibe"
}
```

`POST /v1/captures`
Records raw image as a file.
`GET /v1/captures?processor={processor_id}`
Get all raw images as a file applying the processor to all images
`GET /v1/captures/{capture_id}/?processor={processor_id}`
Get specified image as a file applying the processor

### Processors
Processors are records of image processing parameters applied to an image. Processors are bound to a capture resource in a `capture` and `model` resource to recreate an image record to specification. This endpoint should be easy to scale to support new image processing features. All image processing techniques should be optional however we should require a single technique specification in a post request.

`GET /v1/processors`
Get parameters of all image processing records -> [{...},...]
`GET /v1/processors/{processors_id}`
Get parameters of a single processor instance -> {...}
`POST /v1/processors`
Create a new image processor record
```py
{
   "gaussian_blur": {
      "kernel_width": 3,
      "kernel_height": 3
   },
   "dialation": {
      "kernel_width": 3,
      "kernel_height": 3,
      "iterations": 20
   }, 
   "erosion": {
      "kernel_width": 3,
      "kernel_height": 3,
      "iterations": 20
   },
}
```