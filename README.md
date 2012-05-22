Pollux'NZ City -- Alpha version
===============================

This version of the code of pollux'nz city has been built for a demonstrator
based on a shield featuring several sensors breakout boards, a RF slave shield
and a RF Master/Ethernet shield from our friends at Snootlab.

This demonstrator is a Proof-of-Concept of the Pollux'nz city platform that
will be available on http://www.polluxnzcity.net/

Source tree description
=======================

    .
    |-- PolluxSensor
    |-- PolluxGate
    `-- PolluxInTheCloud

 * PolluxSensor is where lays the code that commands the sensors and processes
    the measures to be sent through RF.
 * PolluxGate is the code of the gateway, between RF and the greats Internets.
 * PolluxInTheCloud is the code of the platform that shows nice charts of the
    measurements done.

Launch me !
===========

just executes:

 % PolluxInTheCloud/polluxinthecloud_launcher.sh

and the software will be run and a browser will be launched (only on debian and
ubuntu linux). Read the script to learn how to manually launch the software.

N.B.: Once you have successfully launched the script, you can start the Pollux 
Gate hardware (the one that is connected to the computer).

Build me !
==========

Open PolluxSensor/PolluxSensor.pde or PolluxGate/PolluxGate.pde in your Arduino
IDE and build/upload it. You can also use the given Makefile.

License
=======

Pollux'NZ City -- Proof of Concept -- source code

(c) 2012 CKAB / hackable:Devices
(c) 2012 Bernard Pratz <guyzmo{at}hackable-devices{dot}org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

