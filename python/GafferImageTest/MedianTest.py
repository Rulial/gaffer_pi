##########################################################################
#
#  Copyright (c) 2017, Image Engine Design Inc. All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#      * Redistributions of source code must retain the above
#        copyright notice, this list of conditions and the following
#        disclaimer.
#
#      * Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials provided with
#        the distribution.
#
#      * Neither the name of John Haddon nor the names of
#        any other contributors to this software may be used to endorse or
#        promote products derived from this software without specific prior
#        written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
##########################################################################

import os
import unittest

import IECore

import Gaffer
import GafferTest
import GafferImage
import GafferImageTest

class MedianTest( GafferImageTest.ImageTestCase ) :

	def testPassThrough( self ) :

		c = GafferImage.Constant()

		m = GafferImage.Median()
		m["in"].setInput( c["out"] )
		m["radius"].setValue( IECore.V2i( 0 ) )

		self.assertEqual( c["out"].imageHash(), m["out"].imageHash() )
		self.assertImagesEqual( c["out"], m["out"] )

	def testExpandDataWindow( self ) :

		c = GafferImage.Constant()

		m = GafferImage.Median()
		m["in"].setInput( c["out"] )
		m["radius"].setValue( IECore.V2i( 1 ) )

		self.assertEqual( m["out"]["dataWindow"].getValue(), c["out"]["dataWindow"].getValue() )

		m["expandDataWindow"].setValue( True )

		self.assertEqual( m["out"]["dataWindow"].getValue().min, c["out"]["dataWindow"].getValue().min - IECore.V2i( 1 ) )
		self.assertEqual( m["out"]["dataWindow"].getValue().max, c["out"]["dataWindow"].getValue().max + IECore.V2i( 1 ) )

	def testFilter( self ) :

		r = GafferImage.ImageReader()
		r["fileName"].setValue( os.path.dirname( __file__ ) + "/images/noisyRamp.exr" )

		m = GafferImage.Median()
		m["in"].setInput( r["out"] )
		self.assertImagesEqual( m["out"], r["out"] )

		m["radius"].setValue( IECore.V2i( 1 ) )
		m["boundingMode"].setValue( GafferImage.Sampler.BoundingMode.Clamp )

		dataWindow = m["out"]["dataWindow"].getValue()
		s = GafferImage.Sampler( m["out"], "R", dataWindow )

		uStep = 1.0 / dataWindow.size().x
		uMin = 0.5 * uStep
		for y in range( dataWindow.min.y, dataWindow.max.y ) :
			for x in range( dataWindow.min.x, dataWindow.max.x ) :
				self.assertAlmostEqual( s.sample( x, y ), uMin + x * uStep, delta = 0.011 )

if __name__ == "__main__":
	unittest.main()
