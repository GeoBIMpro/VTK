#!/usr/bin/env python
import vtk
from vtk.test import Testing
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()

# Create a gaussian
gs = vtk.vtkImageGaussianSource()
gs.SetWholeExtent(0,30,0,30,0,30)
gs.SetMaximum(255.0)
gs.SetStandardDeviation(5)
gs.SetCenter(15,15,15)
# threshold to leave a gap that should show up for
# gradient opacity
t = vtk.vtkImageThreshold()
t.SetInputConnection(gs.GetOutputPort())
t.ReplaceInOn()
t.SetInValue(0)
t.ThresholdBetween(150,200)
# Use a shift scale to convert to unsigned char
ss = vtk.vtkImageShiftScale()
ss.SetInputConnection(t.GetOutputPort())
ss.SetOutputScalarTypeToUnsignedChar()
# grid will be used for two component dependent
grid0 = vtk.vtkImageGridSource()
grid0.SetDataScalarTypeToUnsignedChar()
grid0.SetGridSpacing(10,10,10)
grid0.SetLineValue(200)
grid0.SetFillValue(10)
grid0.SetDataExtent(0,30,0,30,0,30)
# use dilation to thicken the grid
d = vtk.vtkImageContinuousDilate3D()
d.SetInputConnection(grid0.GetOutputPort())
d.SetKernelSize(3,3,3)
# Now make a two component dependent
iac = vtk.vtkImageAppendComponents()
iac.AddInputConnection(d.GetOutputPort())
iac.AddInputConnection(ss.GetOutputPort())
# Some more gaussians for the four component indepent case
gs1 = vtk.vtkImageGaussianSource()
gs1.SetWholeExtent(0,30,0,30,0,30)
gs1.SetMaximum(255.0)
gs1.SetStandardDeviation(4)
gs1.SetCenter(5,5,5)
t1 = vtk.vtkImageThreshold()
t1.SetInputConnection(gs1.GetOutputPort())
t1.ReplaceInOn()
t1.SetInValue(0)
t1.ThresholdBetween(150,256)
gs2 = vtk.vtkImageGaussianSource()
gs2.SetWholeExtent(0,30,0,30,0,30)
gs2.SetMaximum(255.0)
gs2.SetStandardDeviation(4)
gs2.SetCenter(12,12,12)
gs3 = vtk.vtkImageGaussianSource()
gs3.SetWholeExtent(0,30,0,30,0,30)
gs3.SetMaximum(255.0)
gs3.SetStandardDeviation(4)
gs3.SetCenter(19,19,19)
t3 = vtk.vtkImageThreshold()
t3.SetInputConnection(gs3.GetOutputPort())
t3.ReplaceInOn()
t3.SetInValue(0)
t3.ThresholdBetween(150,256)
gs4 = vtk.vtkImageGaussianSource()
gs4.SetWholeExtent(0,30,0,30,0,30)
gs4.SetMaximum(255.0)
gs4.SetStandardDeviation(4)
gs4.SetCenter(26,26,26)
# we need a few append filters ...
iac1 = vtk.vtkImageAppendComponents()
iac1.AddInputConnection(t1.GetOutputPort())
iac1.AddInputConnection(gs2.GetOutputPort())
iac2 = vtk.vtkImageAppendComponents()
iac2.AddInputConnection(iac1.GetOutputPort())
iac2.AddInputConnection(t3.GetOutputPort())
iac3 = vtk.vtkImageAppendComponents()
iac3.AddInputConnection(iac2.GetOutputPort())
iac3.AddInputConnection(gs4.GetOutputPort())
# create the four component dependend -
# use lines in x, y, z for colors
gridR = vtk.vtkImageGridSource()
gridR.SetDataScalarTypeToUnsignedChar()
gridR.SetGridSpacing(10,100,100)
gridR.SetLineValue(250)
gridR.SetFillValue(100)
gridR.SetDataExtent(0,30,0,30,0,30)
dR = vtk.vtkImageContinuousDilate3D()
dR.SetInputConnection(gridR.GetOutputPort())
dR.SetKernelSize(2,2,2)
gridG = vtk.vtkImageGridSource()
gridG.SetDataScalarTypeToUnsignedChar()
gridG.SetGridSpacing(100,10,100)
gridG.SetLineValue(250)
gridG.SetFillValue(100)
gridG.SetDataExtent(0,30,0,30,0,30)
dG = vtk.vtkImageContinuousDilate3D()
dG.SetInputConnection(gridG.GetOutputPort())
dG.SetKernelSize(2,2,2)
gridB = vtk.vtkImageGridSource()
gridB.SetDataScalarTypeToUnsignedChar()
gridB.SetGridSpacing(100,100,10)
gridB.SetLineValue(0)
gridB.SetFillValue(250)
gridB.SetDataExtent(0,30,0,30,0,30)
dB = vtk.vtkImageContinuousDilate3D()
dB.SetInputConnection(gridB.GetOutputPort())
dB.SetKernelSize(2,2,2)
# need some appending
iacRG = vtk.vtkImageAppendComponents()
iacRG.AddInputConnection(dR.GetOutputPort())
iacRG.AddInputConnection(dG.GetOutputPort())
iacRGB = vtk.vtkImageAppendComponents()
iacRGB.AddInputConnection(iacRG.GetOutputPort())
iacRGB.AddInputConnection(dB.GetOutputPort())
iacRGBA = vtk.vtkImageAppendComponents()
iacRGBA.AddInputConnection(iacRGB.GetOutputPort())
iacRGBA.AddInputConnection(ss.GetOutputPort())
# We need a bunch of opacity functions
# this one is a simple ramp to .2
rampPoint2 = vtk.vtkPiecewiseFunction()
rampPoint2.AddPoint(0,0.0)
rampPoint2.AddPoint(255,0.2)
# this one is a simple ramp to 1
ramp1 = vtk.vtkPiecewiseFunction()
ramp1.AddPoint(0,0.0)
ramp1.AddPoint(255,1.0)
# this one shows a sharp surface
surface = vtk.vtkPiecewiseFunction()
surface.AddPoint(0,0.0)
surface.AddPoint(10,0.0)
surface.AddPoint(50,1.0)
surface.AddPoint(255,1.0)
# this one is constant 1
constant1 = vtk.vtkPiecewiseFunction()
constant1.AddPoint(0,1.0)
constant1.AddPoint(255,1.0)
# this one is used for gradient opacity
gop = vtk.vtkPiecewiseFunction()
gop.AddPoint(0,0.0)
gop.AddPoint(20,0.0)
gop.AddPoint(60,1.0)
gop.AddPoint(255,1.0)
# We need a bunch of color functions
# This one is a simple rainbow
rainbow = vtk.vtkColorTransferFunction()
rainbow.SetColorSpaceToHSV()
rainbow.HSVWrapOff()
rainbow.AddHSVPoint(0,0.1,1.0,1.0)
rainbow.AddHSVPoint(255,0.9,1.0,1.0)
# this is constant red
red = vtk.vtkColorTransferFunction()
red.AddRGBPoint(0,1,0,0)
red.AddRGBPoint(255,1,0,0)
# this is constant green
green = vtk.vtkColorTransferFunction()
green.AddRGBPoint(0,0,1,0)
green.AddRGBPoint(255,0,1,0)
# this is constant blue
blue = vtk.vtkColorTransferFunction()
blue.AddRGBPoint(0,0,0,1)
blue.AddRGBPoint(255,0,0,1)
# this is constant yellow
yellow = vtk.vtkColorTransferFunction()
yellow.AddRGBPoint(0,1,1,0)
yellow.AddRGBPoint(255,1,1,0)
ren1 = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.SetSize(500,500)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
ren1.GetCullers().InitTraversal()
culler = ren1.GetCullers().GetNextItem()
culler.SetSortingStyleToBackToFront()
# We need 25 mapper / actor pairs which we will render
# in a grid. Going down we will vary the input data
# with the top row unsigned char, then float, then
# two dependent components, then four dependent components
# then four independent components. Going across we
# will vary the rendering method with MIP, Composite,
# Composite Shade, Composite GO, and Composite GO Shade.
j = 0
while j < 5:
    i = 0
    while i < 5:
        locals()[get_variable_name("volumeProperty", i, "", j, "")] = vtk.vtkVolumeProperty()
        locals()[get_variable_name("volumeMapper", i, "", j, "")] = vtk.vtkFixedPointVolumeRayCastMapper()
        locals()[get_variable_name("volumeMapper", i, "", j, "")].SetSampleDistance(0.25)
        locals()[get_variable_name("volume", i, "", j, "")] = vtk.vtkVolume()
        locals()[get_variable_name("volume", i, "", j, "")].SetMapper(locals()[get_variable_name("volumeMapper", i, "", j, "")])
        locals()[get_variable_name("volume", i, "", j, "")].SetProperty(locals()[get_variable_name("volumeProperty", i, "", j, "")])
        locals()[get_variable_name("volume", i, "", j, "")].AddPosition(expr.expr(globals(), locals(),["i","*","30"]),expr.expr(globals(), locals(),["j","*","30"]),0)
        ren1.AddVolume(locals()[get_variable_name("volume", i, "", j, "")])
        i = i + 1

    j = j + 1

i = 0
while i < 5:
    locals()[get_variable_name("volumeMapper0", i, "")].SetInputConnection(t.GetOutputPort())
    locals()[get_variable_name("volumeMapper1", i, "")].SetInputConnection(ss.GetOutputPort())
    locals()[get_variable_name("volumeMapper2", i, "")].SetInputConnection(iac.GetOutputPort())
    locals()[get_variable_name("volumeMapper3", i, "")].SetInputConnection(iac3.GetOutputPort())
    locals()[get_variable_name("volumeMapper4", i, "")].SetInputConnection(iacRGBA.GetOutputPort())
    locals()[get_variable_name("volumeMapper", i, "0")].SetBlendModeToMaximumIntensity()
    locals()[get_variable_name("volumeMapper", i, "1")].SetBlendModeToComposite()
    locals()[get_variable_name("volumeMapper", i, "2")].SetBlendModeToComposite()
    locals()[get_variable_name("volumeMapper", i, "3")].SetBlendModeToComposite()
    locals()[get_variable_name("volumeMapper", i, "4")].SetBlendModeToComposite()
    locals()[get_variable_name("volumeProperty0", i, "")].IndependentComponentsOn()
    locals()[get_variable_name("volumeProperty1", i, "")].IndependentComponentsOn()
    locals()[get_variable_name("volumeProperty2", i, "")].IndependentComponentsOff()
    locals()[get_variable_name("volumeProperty3", i, "")].IndependentComponentsOn()
    locals()[get_variable_name("volumeProperty4", i, "")].IndependentComponentsOff()
    locals()[get_variable_name("volumeProperty0", i, "")].SetColor(rainbow)
    locals()[get_variable_name("volumeProperty0", i, "")].SetScalarOpacity(rampPoint2)
    locals()[get_variable_name("volumeProperty0", i, "")].SetGradientOpacity(constant1)
    locals()[get_variable_name("volumeProperty1", i, "")].SetColor(rainbow)
    locals()[get_variable_name("volumeProperty1", i, "")].SetScalarOpacity(rampPoint2)
    locals()[get_variable_name("volumeProperty1", i, "")].SetGradientOpacity(constant1)
    locals()[get_variable_name("volumeProperty2", i, "")].SetColor(rainbow)
    locals()[get_variable_name("volumeProperty2", i, "")].SetScalarOpacity(rampPoint2)
    locals()[get_variable_name("volumeProperty2", i, "")].SetGradientOpacity(constant1)
    locals()[get_variable_name("volumeProperty3", i, "")].SetColor(0,red)
    locals()[get_variable_name("volumeProperty3", i, "")].SetColor(1,green)
    locals()[get_variable_name("volumeProperty3", i, "")].SetColor(2,blue)
    locals()[get_variable_name("volumeProperty3", i, "")].SetColor(3,yellow)
    locals()[get_variable_name("volumeProperty3", i, "")].SetScalarOpacity(0,rampPoint2)
    locals()[get_variable_name("volumeProperty3", i, "")].SetScalarOpacity(1,rampPoint2)
    locals()[get_variable_name("volumeProperty3", i, "")].SetScalarOpacity(2,rampPoint2)
    locals()[get_variable_name("volumeProperty3", i, "")].SetScalarOpacity(3,rampPoint2)
    locals()[get_variable_name("volumeProperty3", i, "")].SetGradientOpacity(0,constant1)
    locals()[get_variable_name("volumeProperty3", i, "")].SetGradientOpacity(1,constant1)
    locals()[get_variable_name("volumeProperty3", i, "")].SetGradientOpacity(2,constant1)
    locals()[get_variable_name("volumeProperty3", i, "")].SetGradientOpacity(3,constant1)
    locals()[get_variable_name("volumeProperty3", i, "")].SetComponentWeight(0,1)
    locals()[get_variable_name("volumeProperty3", i, "")].SetComponentWeight(1,1)
    locals()[get_variable_name("volumeProperty3", i, "")].SetComponentWeight(2,1)
    locals()[get_variable_name("volumeProperty3", i, "")].SetComponentWeight(3,1)
    locals()[get_variable_name("volumeProperty4", i, "")].SetColor(rainbow)
    locals()[get_variable_name("volumeProperty4", i, "")].SetScalarOpacity(rampPoint2)
    locals()[get_variable_name("volumeProperty4", i, "")].SetGradientOpacity(constant1)
    locals()[get_variable_name("volumeProperty", i, "2")].ShadeOn()
    locals()[get_variable_name("volumeProperty", i, "4")].ShadeOn(0)
    locals()[get_variable_name("volumeProperty", i, "4")].ShadeOn(1)
    locals()[get_variable_name("volumeProperty", i, "4")].ShadeOn(2)
    locals()[get_variable_name("volumeProperty", i, "4")].ShadeOn(3)
    i = i + 1

volumeProperty00.SetScalarOpacity(ramp1)
volumeProperty10.SetScalarOpacity(ramp1)
volumeProperty20.SetScalarOpacity(ramp1)
volumeProperty30.SetScalarOpacity(0,surface)
volumeProperty30.SetScalarOpacity(1,surface)
volumeProperty30.SetScalarOpacity(2,surface)
volumeProperty30.SetScalarOpacity(3,surface)
volumeProperty40.SetScalarOpacity(ramp1)
volumeProperty02.SetScalarOpacity(surface)
volumeProperty12.SetScalarOpacity(surface)
volumeProperty22.SetScalarOpacity(surface)
volumeProperty32.SetScalarOpacity(0,surface)
volumeProperty32.SetScalarOpacity(1,surface)
volumeProperty32.SetScalarOpacity(2,surface)
volumeProperty32.SetScalarOpacity(3,surface)
volumeProperty42.SetScalarOpacity(surface)
volumeProperty04.SetScalarOpacity(surface)
volumeProperty14.SetScalarOpacity(surface)
volumeProperty24.SetScalarOpacity(surface)
volumeProperty34.SetScalarOpacity(0,surface)
volumeProperty34.SetScalarOpacity(1,surface)
volumeProperty34.SetScalarOpacity(2,surface)
volumeProperty34.SetScalarOpacity(3,surface)
volumeProperty44.SetScalarOpacity(surface)
volumeProperty03.SetGradientOpacity(gop)
volumeProperty13.SetGradientOpacity(gop)
volumeProperty23.SetGradientOpacity(gop)
volumeProperty33.SetGradientOpacity(0,gop)
volumeProperty33.SetGradientOpacity(2,gop)
volumeProperty43.SetGradientOpacity(gop)
volumeProperty33.SetScalarOpacity(0,ramp1)
volumeProperty33.SetScalarOpacity(2,ramp1)
volumeProperty04.SetGradientOpacity(gop)
volumeProperty14.SetGradientOpacity(gop)
volumeProperty24.SetGradientOpacity(gop)
volumeProperty34.SetGradientOpacity(0,gop)
volumeProperty34.SetGradientOpacity(2,gop)
volumeProperty44.SetGradientOpacity(gop)
renWin.Render()
ren1.GetActiveCamera().Dolly(1.3)
ren1.GetActiveCamera().Azimuth(15)
ren1.GetActiveCamera().Elevation(5)
ren1.ResetCameraClippingRange()
iren.Initialize()
# --- end of script --
