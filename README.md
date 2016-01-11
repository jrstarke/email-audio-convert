# email-audio-convert

A lambda function for receiving Simple Email Service messages via SNS,
converting any wave files to mp3 before sending the message on.

## Requirements

ffmpeg should be available within your path. If you do not have ffmpeg installed
in your system, such as on Lambda, you can place a compiled binary in the `lib` folder.

I have had success with the binary available at http://johnvansickle.com/ffmpeg/

## audio_convert.py

This is the core of this function. It receives an SNS message, retrieves the original email message,
creates a new message with a To address based on the original To address, a From message that is 
equivalent to the To of the original, and sets the Reply-To to the original From address. It then
looks for any attached wave files, and converts them to MP3 before sending them on.

## library_location.py

This is a helper module that allows for checking for the availability of a library, and if it is not
available on the system path by default, adds a path to the system path and checks for the library.


-----

Copyright 2015 Jamie Starke.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
