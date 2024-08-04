#!/bin/env python

# Python bindings for OpenVR API version 0.9.20
# from https://github.com/ValveSoftware/openvr
# Created May 7, 2016 Christopher Bruns

import os
import platform
import ctypes
from ctypes import *

from .version import __version__

####################################################################
### Load OpenVR shared library, so we can access it using ctypes ###
####################################################################

# Detect 32-bit vs 64-bit python
# Detect platform
if sizeof(c_void_p) == 4:
    if platform.system() == 'Windows':
        _openvr_lib_name = "libopenvr_api_32"
    elif platform.system() == 'Linux':
        _openvr_lib_name = "libopenvr_api_32.so"
    elif platform.system() == 'Darwin':
        _openvr_lib_name = "libopenvr_api_32.dylib"    
    else:
        raise ValueError("Libraries not available for this platform: " + platform.system())
else:
    if platform.system() == 'Windows':
        _openvr_lib_name = "libopenvr_api_64"
    elif platform.system() == 'Linux':
        _openvr_lib_name = "libopenvr_api_64.so"
    else:
        raise ValueError("Libraries not available for this platform: " + platform.system())

# Add current directory to PATH, so we can load the DLL from right here.
os.environ['PATH'] += os.pathsep + os.path.dirname(__file__)
_openvr = cdll.LoadLibrary(_openvr_lib_name)

# Function pointer table calling convention
if platform.system() == 'Windows':
    OPENVR_FNTABLE_CALLTYPE = WINFUNCTYPE # __stdcall in openvr_capi.h
else:
    OPENVR_FNTABLE_CALLTYPE = CFUNCTYPE # __cdecl
    
# Forward declarations for Vulkan structures
class VkDevice_T(ctypes.Structure):
    pass
    
class VkPhysicalDevice_T(ctypes.Structure):
    pass

class VkInstance_T(ctypes.Structure):
    pass

class VkQueue_T(ctypes.Structure):
    pass


# Forward declarations for Direct3D structures

class ID3D12Resource(ctypes.Structure):
    pass

class ID3D12CommandQueue(ctypes.Structure):
    pass


########################
### Expose constants ###
########################

k_unMaxDriverDebugResponseSize = 32768
k_unTrackedDeviceIndex_Hmd = 0
k_unMaxTrackedDeviceCount = 16
k_unTrackedDeviceIndexOther = 4294967294
k_unTrackedDeviceIndexInvalid = 4294967295
k_ulInvalidPropertyContainer = 0
k_unInvalidPropertyTag = 0
k_unFloatPropertyTag = 1
k_unInt32PropertyTag = 2
k_unUint64PropertyTag = 3
k_unBoolPropertyTag = 4
k_unStringPropertyTag = 5
k_unHmdMatrix34PropertyTag = 20
k_unHmdMatrix44PropertyTag = 21
k_unHmdVector3PropertyTag = 22
k_unHmdVector4PropertyTag = 23
k_unHiddenAreaPropertyTag = 30
k_unOpenVRInternalReserved_Start = 1000
k_unOpenVRInternalReserved_End = 10000
k_unMaxPropertyStringSize = 32768
k_unControllerStateAxisCount = 5
k_ulOverlayHandleInvalid = 0
k_unScreenshotHandleInvalid = 0
IVRSystem_Version = b"IVRSystem_015"
IVRExtendedDisplay_Version = b"IVRExtendedDisplay_001"
IVRTrackedCamera_Version = b"IVRTrackedCamera_003"
k_unMaxApplicationKeyLength = 128
k_pch_MimeType_HomeApp = b"vr/home"
k_pch_MimeType_GameTheater = b"vr/game_theater"
IVRApplications_Version = b"IVRApplications_006"
IVRChaperone_Version = b"IVRChaperone_003"
IVRChaperoneSetup_Version = b"IVRChaperoneSetup_005"
IVRCompositor_Version = b"IVRCompositor_020"
k_unVROverlayMaxKeyLength = 128
k_unVROverlayMaxNameLength = 128
k_unMaxOverlayCount = 64
k_unMaxOverlayIntersectionMaskPrimitivesCount = 32
IVROverlay_Version = b"IVROverlay_016"
k_pch_Controller_Component_GDC2015 = b"gdc2015"
k_pch_Controller_Component_Base = b"base"
k_pch_Controller_Component_Tip = b"tip"
k_pch_Controller_Component_HandGrip = b"handgrip"
k_pch_Controller_Component_Status = b"status"
IVRRenderModels_Version = b"IVRRenderModels_005"
k_unNotificationTextMaxSize = 256
IVRNotifications_Version = b"IVRNotifications_002"
k_unMaxSettingsKeyLength = 128
IVRSettings_Version = b"IVRSettings_002"
k_pch_SteamVR_Section = b"steamvr"
k_pch_SteamVR_RequireHmd_String = b"requireHmd"
k_pch_SteamVR_ForcedDriverKey_String = b"forcedDriver"
k_pch_SteamVR_ForcedHmdKey_String = b"forcedHmd"
k_pch_SteamVR_DisplayDebug_Bool = b"displayDebug"
k_pch_SteamVR_DebugProcessPipe_String = b"debugProcessPipe"
k_pch_SteamVR_DisplayDebugX_Int32 = b"displayDebugX"
k_pch_SteamVR_DisplayDebugY_Int32 = b"displayDebugY"
k_pch_SteamVR_SendSystemButtonToAllApps_Bool = b"sendSystemButtonToAllApps"
k_pch_SteamVR_LogLevel_Int32 = b"loglevel"
k_pch_SteamVR_IPD_Float = b"ipd"
k_pch_SteamVR_Background_String = b"background"
k_pch_SteamVR_BackgroundUseDomeProjection_Bool = b"backgroundUseDomeProjection"
k_pch_SteamVR_BackgroundCameraHeight_Float = b"backgroundCameraHeight"
k_pch_SteamVR_BackgroundDomeRadius_Float = b"backgroundDomeRadius"
k_pch_SteamVR_GridColor_String = b"gridColor"
k_pch_SteamVR_PlayAreaColor_String = b"playAreaColor"
k_pch_SteamVR_ShowStage_Bool = b"showStage"
k_pch_SteamVR_ActivateMultipleDrivers_Bool = b"activateMultipleDrivers"
k_pch_SteamVR_DirectMode_Bool = b"directMode"
k_pch_SteamVR_DirectModeEdidVid_Int32 = b"directModeEdidVid"
k_pch_SteamVR_DirectModeEdidPid_Int32 = b"directModeEdidPid"
k_pch_SteamVR_UsingSpeakers_Bool = b"usingSpeakers"
k_pch_SteamVR_SpeakersForwardYawOffsetDegrees_Float = b"speakersForwardYawOffsetDegrees"
k_pch_SteamVR_BaseStationPowerManagement_Bool = b"basestationPowerManagement"
k_pch_SteamVR_NeverKillProcesses_Bool = b"neverKillProcesses"
k_pch_SteamVR_RenderTargetMultiplier_Float = b"renderTargetMultiplier"
k_pch_SteamVR_AllowAsyncReprojection_Bool = b"allowAsyncReprojection"
k_pch_SteamVR_AllowReprojection_Bool = b"allowInterleavedReprojection"
k_pch_SteamVR_ForceReprojection_Bool = b"forceReprojection"
k_pch_SteamVR_ForceFadeOnBadTracking_Bool = b"forceFadeOnBadTracking"
k_pch_SteamVR_DefaultMirrorView_Int32 = b"defaultMirrorView"
k_pch_SteamVR_ShowMirrorView_Bool = b"showMirrorView"
k_pch_SteamVR_MirrorViewGeometry_String = b"mirrorViewGeometry"
k_pch_SteamVR_StartMonitorFromAppLaunch = b"startMonitorFromAppLaunch"
k_pch_SteamVR_StartCompositorFromAppLaunch_Bool = b"startCompositorFromAppLaunch"
k_pch_SteamVR_StartDashboardFromAppLaunch_Bool = b"startDashboardFromAppLaunch"
k_pch_SteamVR_StartOverlayAppsFromDashboard_Bool = b"startOverlayAppsFromDashboard"
k_pch_SteamVR_EnableHomeApp = b"enableHomeApp"
k_pch_SteamVR_SetInitialDefaultHomeApp = b"setInitialDefaultHomeApp"
k_pch_SteamVR_CycleBackgroundImageTimeSec_Int32 = b"CycleBackgroundImageTimeSec"
k_pch_SteamVR_RetailDemo_Bool = b"retailDemo"
k_pch_SteamVR_IpdOffset_Float = b"ipdOffset"
k_pch_Lighthouse_Section = b"driver_lighthouse"
k_pch_Lighthouse_DisableIMU_Bool = b"disableimu"
k_pch_Lighthouse_UseDisambiguation_String = b"usedisambiguation"
k_pch_Lighthouse_DisambiguationDebug_Int32 = b"disambiguationdebug"
k_pch_Lighthouse_PrimaryBasestation_Int32 = b"primarybasestation"
k_pch_Lighthouse_DBHistory_Bool = b"dbhistory"
k_pch_Null_Section = b"driver_null"
k_pch_Null_SerialNumber_String = b"serialNumber"
k_pch_Null_ModelNumber_String = b"modelNumber"
k_pch_Null_WindowX_Int32 = b"windowX"
k_pch_Null_WindowY_Int32 = b"windowY"
k_pch_Null_WindowWidth_Int32 = b"windowWidth"
k_pch_Null_WindowHeight_Int32 = b"windowHeight"
k_pch_Null_RenderWidth_Int32 = b"renderWidth"
k_pch_Null_RenderHeight_Int32 = b"renderHeight"
k_pch_Null_SecondsFromVsyncToPhotons_Float = b"secondsFromVsyncToPhotons"
k_pch_Null_DisplayFrequency_Float = b"displayFrequency"
k_pch_UserInterface_Section = b"userinterface"
k_pch_UserInterface_StatusAlwaysOnTop_Bool = b"StatusAlwaysOnTop"
k_pch_UserInterface_MinimizeToTray_Bool = b"MinimizeToTray"
k_pch_UserInterface_Screenshots_Bool = b"screenshots"
k_pch_UserInterface_ScreenshotType_Int = b"screenshotType"
k_pch_Notifications_Section = b"notifications"
k_pch_Notifications_DoNotDisturb_Bool = b"DoNotDisturb"
k_pch_Keyboard_Section = b"keyboard"
k_pch_Keyboard_TutorialCompletions = b"TutorialCompletions"
k_pch_Keyboard_ScaleX = b"ScaleX"
k_pch_Keyboard_ScaleY = b"ScaleY"
k_pch_Keyboard_OffsetLeftX = b"OffsetLeftX"
k_pch_Keyboard_OffsetRightX = b"OffsetRightX"
k_pch_Keyboard_OffsetY = b"OffsetY"
k_pch_Keyboard_Smoothing = b"Smoothing"
k_pch_Perf_Section = b"perfcheck"
k_pch_Perf_HeuristicActive_Bool = b"heuristicActive"
k_pch_Perf_NotifyInHMD_Bool = b"warnInHMD"
k_pch_Perf_NotifyOnlyOnce_Bool = b"warnOnlyOnce"
k_pch_Perf_AllowTimingStore_Bool = b"allowTimingStore"
k_pch_Perf_SaveTimingsOnExit_Bool = b"saveTimingsOnExit"
k_pch_Perf_TestData_Float = b"perfTestData"
k_pch_CollisionBounds_Section = b"collisionBounds"
k_pch_CollisionBounds_Style_Int32 = b"CollisionBoundsStyle"
k_pch_CollisionBounds_GroundPerimeterOn_Bool = b"CollisionBoundsGroundPerimeterOn"
k_pch_CollisionBounds_CenterMarkerOn_Bool = b"CollisionBoundsCenterMarkerOn"
k_pch_CollisionBounds_PlaySpaceOn_Bool = b"CollisionBoundsPlaySpaceOn"
k_pch_CollisionBounds_FadeDistance_Float = b"CollisionBoundsFadeDistance"
k_pch_CollisionBounds_ColorGammaR_Int32 = b"CollisionBoundsColorGammaR"
k_pch_CollisionBounds_ColorGammaG_Int32 = b"CollisionBoundsColorGammaG"
k_pch_CollisionBounds_ColorGammaB_Int32 = b"CollisionBoundsColorGammaB"
k_pch_CollisionBounds_ColorGammaA_Int32 = b"CollisionBoundsColorGammaA"
k_pch_Camera_Section = b"camera"
k_pch_Camera_EnableCamera_Bool = b"enableCamera"
k_pch_Camera_EnableCameraInDashboard_Bool = b"enableCameraInDashboard"
k_pch_Camera_EnableCameraForCollisionBounds_Bool = b"enableCameraForCollisionBounds"
k_pch_Camera_EnableCameraForRoomView_Bool = b"enableCameraForRoomView"
k_pch_Camera_BoundsColorGammaR_Int32 = b"cameraBoundsColorGammaR"
k_pch_Camera_BoundsColorGammaG_Int32 = b"cameraBoundsColorGammaG"
k_pch_Camera_BoundsColorGammaB_Int32 = b"cameraBoundsColorGammaB"
k_pch_Camera_BoundsColorGammaA_Int32 = b"cameraBoundsColorGammaA"
k_pch_Camera_BoundsStrength_Int32 = b"cameraBoundsStrength"
k_pch_audio_Section = b"audio"
k_pch_audio_OnPlaybackDevice_String = b"onPlaybackDevice"
k_pch_audio_OnRecordDevice_String = b"onRecordDevice"
k_pch_audio_OnPlaybackMirrorDevice_String = b"onPlaybackMirrorDevice"
k_pch_audio_OffPlaybackDevice_String = b"offPlaybackDevice"
k_pch_audio_OffRecordDevice_String = b"offRecordDevice"
k_pch_audio_VIVEHDMIGain = b"viveHDMIGain"
k_pch_Power_Section = b"power"
k_pch_Power_PowerOffOnExit_Bool = b"powerOffOnExit"
k_pch_Power_TurnOffScreensTimeout_Float = b"turnOffScreensTimeout"
k_pch_Power_TurnOffControllersTimeout_Float = b"turnOffControllersTimeout"
k_pch_Power_ReturnToWatchdogTimeout_Float = b"returnToWatchdogTimeout"
k_pch_Power_AutoLaunchSteamVROnButtonPress = b"autoLaunchSteamVROnButtonPress"
k_pch_Dashboard_Section = b"dashboard"
k_pch_Dashboard_EnableDashboard_Bool = b"enableDashboard"
k_pch_Dashboard_ArcadeMode_Bool = b"arcadeMode"
k_pch_modelskin_Section = b"modelskins"
k_pch_Driver_Enable_Bool = b"enable"
IVRScreenshots_Version = b"IVRScreenshots_001"
IVRResources_Version = b"IVRResources_001"

#############################
### Expose enum constants ###
#############################

ENUM_TYPE = c_uint32
ENUM_VALUE_TYPE = int

EVREye = ENUM_TYPE
Eye_Left = ENUM_VALUE_TYPE(0)
Eye_Right = ENUM_VALUE_TYPE(1)

ETextureType = ENUM_TYPE
TextureType_DirectX = ENUM_VALUE_TYPE(0)
TextureType_OpenGL = ENUM_VALUE_TYPE(1)
TextureType_Vulkan = ENUM_VALUE_TYPE(2)
TextureType_IOSurface = ENUM_VALUE_TYPE(3)
TextureType_DirectX12 = ENUM_VALUE_TYPE(4)

EColorSpace = ENUM_TYPE
ColorSpace_Auto = ENUM_VALUE_TYPE(0)
ColorSpace_Gamma = ENUM_VALUE_TYPE(1)
ColorSpace_Linear = ENUM_VALUE_TYPE(2)

ETrackingResult = ENUM_TYPE
TrackingResult_Uninitialized = ENUM_VALUE_TYPE(1)
TrackingResult_Calibrating_InProgress = ENUM_VALUE_TYPE(100)
TrackingResult_Calibrating_OutOfRange = ENUM_VALUE_TYPE(101)
TrackingResult_Running_OK = ENUM_VALUE_TYPE(200)
TrackingResult_Running_OutOfRange = ENUM_VALUE_TYPE(201)

ETrackedDeviceClass = ENUM_TYPE
TrackedDeviceClass_Invalid = ENUM_VALUE_TYPE(0)
TrackedDeviceClass_HMD = ENUM_VALUE_TYPE(1)
TrackedDeviceClass_Controller = ENUM_VALUE_TYPE(2)
TrackedDeviceClass_GenericTracker = ENUM_VALUE_TYPE(3)
TrackedDeviceClass_TrackingReference = ENUM_VALUE_TYPE(4)
TrackedDeviceClass_DisplayRedirect = ENUM_VALUE_TYPE(5)

ETrackedControllerRole = ENUM_TYPE
TrackedControllerRole_Invalid = ENUM_VALUE_TYPE(0)
TrackedControllerRole_LeftHand = ENUM_VALUE_TYPE(1)
TrackedControllerRole_RightHand = ENUM_VALUE_TYPE(2)

ETrackingUniverseOrigin = ENUM_TYPE
TrackingUniverseSeated = ENUM_VALUE_TYPE(0)
TrackingUniverseStanding = ENUM_VALUE_TYPE(1)
TrackingUniverseRawAndUncalibrated = ENUM_VALUE_TYPE(2)

ETrackedDeviceProperty = ENUM_TYPE
Prop_Invalid = ENUM_VALUE_TYPE(0)
Prop_TrackingSystemName_String = ENUM_VALUE_TYPE(1000)
Prop_ModelNumber_String = ENUM_VALUE_TYPE(1001)
Prop_SerialNumber_String = ENUM_VALUE_TYPE(1002)
Prop_RenderModelName_String = ENUM_VALUE_TYPE(1003)
Prop_WillDriftInYaw_Bool = ENUM_VALUE_TYPE(1004)
Prop_ManufacturerName_String = ENUM_VALUE_TYPE(1005)
Prop_TrackingFirmwareVersion_String = ENUM_VALUE_TYPE(1006)
Prop_HardwareRevision_String = ENUM_VALUE_TYPE(1007)
Prop_AllWirelessDongleDescriptions_String = ENUM_VALUE_TYPE(1008)
Prop_ConnectedWirelessDongle_String = ENUM_VALUE_TYPE(1009)
Prop_DeviceIsWireless_Bool = ENUM_VALUE_TYPE(1010)
Prop_DeviceIsCharging_Bool = ENUM_VALUE_TYPE(1011)
Prop_DeviceBatteryPercentage_Float = ENUM_VALUE_TYPE(1012)
Prop_StatusDisplayTransform_Matrix34 = ENUM_VALUE_TYPE(1013)
Prop_Firmware_UpdateAvailable_Bool = ENUM_VALUE_TYPE(1014)
Prop_Firmware_ManualUpdate_Bool = ENUM_VALUE_TYPE(1015)
Prop_Firmware_ManualUpdateURL_String = ENUM_VALUE_TYPE(1016)
Prop_HardwareRevision_Uint64 = ENUM_VALUE_TYPE(1017)
Prop_FirmwareVersion_Uint64 = ENUM_VALUE_TYPE(1018)
Prop_FPGAVersion_Uint64 = ENUM_VALUE_TYPE(1019)
Prop_VRCVersion_Uint64 = ENUM_VALUE_TYPE(1020)
Prop_RadioVersion_Uint64 = ENUM_VALUE_TYPE(1021)
Prop_DongleVersion_Uint64 = ENUM_VALUE_TYPE(1022)
Prop_BlockServerShutdown_Bool = ENUM_VALUE_TYPE(1023)
Prop_CanUnifyCoordinateSystemWithHmd_Bool = ENUM_VALUE_TYPE(1024)
Prop_ContainsProximitySensor_Bool = ENUM_VALUE_TYPE(1025)
Prop_DeviceProvidesBatteryStatus_Bool = ENUM_VALUE_TYPE(1026)
Prop_DeviceCanPowerOff_Bool = ENUM_VALUE_TYPE(1027)
Prop_Firmware_ProgrammingTarget_String = ENUM_VALUE_TYPE(1028)
Prop_DeviceClass_Int32 = ENUM_VALUE_TYPE(1029)
Prop_HasCamera_Bool = ENUM_VALUE_TYPE(1030)
Prop_DriverVersion_String = ENUM_VALUE_TYPE(1031)
Prop_Firmware_ForceUpdateRequired_Bool = ENUM_VALUE_TYPE(1032)
Prop_ViveSystemButtonFixRequired_Bool = ENUM_VALUE_TYPE(1033)
Prop_ParentDriver_Uint64 = ENUM_VALUE_TYPE(1034)
Prop_ResourceRoot_String = ENUM_VALUE_TYPE(1035)
Prop_ReportsTimeSinceVSync_Bool = ENUM_VALUE_TYPE(2000)
Prop_SecondsFromVsyncToPhotons_Float = ENUM_VALUE_TYPE(2001)
Prop_DisplayFrequency_Float = ENUM_VALUE_TYPE(2002)
Prop_UserIpdMeters_Float = ENUM_VALUE_TYPE(2003)
Prop_CurrentUniverseId_Uint64 = ENUM_VALUE_TYPE(2004)
Prop_PreviousUniverseId_Uint64 = ENUM_VALUE_TYPE(2005)
Prop_DisplayFirmwareVersion_Uint64 = ENUM_VALUE_TYPE(2006)
Prop_IsOnDesktop_Bool = ENUM_VALUE_TYPE(2007)
Prop_DisplayMCType_Int32 = ENUM_VALUE_TYPE(2008)
Prop_DisplayMCOffset_Float = ENUM_VALUE_TYPE(2009)
Prop_DisplayMCScale_Float = ENUM_VALUE_TYPE(2010)
Prop_EdidVendorID_Int32 = ENUM_VALUE_TYPE(2011)
Prop_DisplayMCImageLeft_String = ENUM_VALUE_TYPE(2012)
Prop_DisplayMCImageRight_String = ENUM_VALUE_TYPE(2013)
Prop_DisplayGCBlackClamp_Float = ENUM_VALUE_TYPE(2014)
Prop_EdidProductID_Int32 = ENUM_VALUE_TYPE(2015)
Prop_CameraToHeadTransform_Matrix34 = ENUM_VALUE_TYPE(2016)
Prop_DisplayGCType_Int32 = ENUM_VALUE_TYPE(2017)
Prop_DisplayGCOffset_Float = ENUM_VALUE_TYPE(2018)
Prop_DisplayGCScale_Float = ENUM_VALUE_TYPE(2019)
Prop_DisplayGCPrescale_Float = ENUM_VALUE_TYPE(2020)
Prop_DisplayGCImage_String = ENUM_VALUE_TYPE(2021)
Prop_LensCenterLeftU_Float = ENUM_VALUE_TYPE(2022)
Prop_LensCenterLeftV_Float = ENUM_VALUE_TYPE(2023)
Prop_LensCenterRightU_Float = ENUM_VALUE_TYPE(2024)
Prop_LensCenterRightV_Float = ENUM_VALUE_TYPE(2025)
Prop_UserHeadToEyeDepthMeters_Float = ENUM_VALUE_TYPE(2026)
Prop_CameraFirmwareVersion_Uint64 = ENUM_VALUE_TYPE(2027)
Prop_CameraFirmwareDescription_String = ENUM_VALUE_TYPE(2028)
Prop_DisplayFPGAVersion_Uint64 = ENUM_VALUE_TYPE(2029)
Prop_DisplayBootloaderVersion_Uint64 = ENUM_VALUE_TYPE(2030)
Prop_DisplayHardwareVersion_Uint64 = ENUM_VALUE_TYPE(2031)
Prop_AudioFirmwareVersion_Uint64 = ENUM_VALUE_TYPE(2032)
Prop_CameraCompatibilityMode_Int32 = ENUM_VALUE_TYPE(2033)
Prop_ScreenshotHorizontalFieldOfViewDegrees_Float = ENUM_VALUE_TYPE(2034)
Prop_ScreenshotVerticalFieldOfViewDegrees_Float = ENUM_VALUE_TYPE(2035)
Prop_DisplaySuppressed_Bool = ENUM_VALUE_TYPE(2036)
Prop_DisplayAllowNightMode_Bool = ENUM_VALUE_TYPE(2037)
Prop_DisplayMCImageWidth_Int32 = ENUM_VALUE_TYPE(2038)
Prop_DisplayMCImageHeight_Int32 = ENUM_VALUE_TYPE(2039)
Prop_DisplayMCImageNumChannels_Int32 = ENUM_VALUE_TYPE(2040)
Prop_DisplayMCImageData_Binary = ENUM_VALUE_TYPE(2041)
Prop_SecondsFromPhotonsToVblank_Float = ENUM_VALUE_TYPE(2042)
Prop_AttachedDeviceId_String = ENUM_VALUE_TYPE(3000)
Prop_SupportedButtons_Uint64 = ENUM_VALUE_TYPE(3001)
Prop_Axis0Type_Int32 = ENUM_VALUE_TYPE(3002)
Prop_Axis1Type_Int32 = ENUM_VALUE_TYPE(3003)
Prop_Axis2Type_Int32 = ENUM_VALUE_TYPE(3004)
Prop_Axis3Type_Int32 = ENUM_VALUE_TYPE(3005)
Prop_Axis4Type_Int32 = ENUM_VALUE_TYPE(3006)
Prop_ControllerRoleHint_Int32 = ENUM_VALUE_TYPE(3007)
Prop_FieldOfViewLeftDegrees_Float = ENUM_VALUE_TYPE(4000)
Prop_FieldOfViewRightDegrees_Float = ENUM_VALUE_TYPE(4001)
Prop_FieldOfViewTopDegrees_Float = ENUM_VALUE_TYPE(4002)
Prop_FieldOfViewBottomDegrees_Float = ENUM_VALUE_TYPE(4003)
Prop_TrackingRangeMinimumMeters_Float = ENUM_VALUE_TYPE(4004)
Prop_TrackingRangeMaximumMeters_Float = ENUM_VALUE_TYPE(4005)
Prop_ModeLabel_String = ENUM_VALUE_TYPE(4006)
Prop_IconPathName_String = ENUM_VALUE_TYPE(5000)
Prop_NamedIconPathDeviceOff_String = ENUM_VALUE_TYPE(5001)
Prop_NamedIconPathDeviceSearching_String = ENUM_VALUE_TYPE(5002)
Prop_NamedIconPathDeviceSearchingAlert_String = ENUM_VALUE_TYPE(5003)
Prop_NamedIconPathDeviceReady_String = ENUM_VALUE_TYPE(5004)
Prop_NamedIconPathDeviceReadyAlert_String = ENUM_VALUE_TYPE(5005)
Prop_NamedIconPathDeviceNotReady_String = ENUM_VALUE_TYPE(5006)
Prop_NamedIconPathDeviceStandby_String = ENUM_VALUE_TYPE(5007)
Prop_NamedIconPathDeviceAlertLow_String = ENUM_VALUE_TYPE(5008)
Prop_DisplayHiddenArea_Binary_Start = ENUM_VALUE_TYPE(5100)
Prop_DisplayHiddenArea_Binary_End = ENUM_VALUE_TYPE(5150)
Prop_UserConfigPath_String = ENUM_VALUE_TYPE(6000)
Prop_InstallPath_String = ENUM_VALUE_TYPE(6001)
Prop_HasDisplayComponent_Bool = ENUM_VALUE_TYPE(6002)
Prop_HasControllerComponent_Bool = ENUM_VALUE_TYPE(6003)
Prop_HasCameraComponent_Bool = ENUM_VALUE_TYPE(6004)
Prop_HasDriverDirectModeComponent_Bool = ENUM_VALUE_TYPE(6005)
Prop_HasVirtualDisplayComponent_Bool = ENUM_VALUE_TYPE(6006)
Prop_VendorSpecific_Reserved_Start = ENUM_VALUE_TYPE(10000)
Prop_VendorSpecific_Reserved_End = ENUM_VALUE_TYPE(10999)

ETrackedPropertyError = ENUM_TYPE
TrackedProp_Success = ENUM_VALUE_TYPE(0)
TrackedProp_WrongDataType = ENUM_VALUE_TYPE(1)
TrackedProp_WrongDeviceClass = ENUM_VALUE_TYPE(2)
TrackedProp_BufferTooSmall = ENUM_VALUE_TYPE(3)
TrackedProp_UnknownProperty = ENUM_VALUE_TYPE(4)
TrackedProp_InvalidDevice = ENUM_VALUE_TYPE(5)
TrackedProp_CouldNotContactServer = ENUM_VALUE_TYPE(6)
TrackedProp_ValueNotProvidedByDevice = ENUM_VALUE_TYPE(7)
TrackedProp_StringExceedsMaximumLength = ENUM_VALUE_TYPE(8)
TrackedProp_NotYetAvailable = ENUM_VALUE_TYPE(9)
TrackedProp_PermissionDenied = ENUM_VALUE_TYPE(10)
TrackedProp_InvalidOperation = ENUM_VALUE_TYPE(11)

EVRSubmitFlags = ENUM_TYPE
Submit_Default = ENUM_VALUE_TYPE(0)
Submit_LensDistortionAlreadyApplied = ENUM_VALUE_TYPE(1)
Submit_GlRenderBuffer = ENUM_VALUE_TYPE(2)
Submit_Reserved = ENUM_VALUE_TYPE(4)

EVRState = ENUM_TYPE
VRState_Undefined = ENUM_VALUE_TYPE(-1)
VRState_Off = ENUM_VALUE_TYPE(0)
VRState_Searching = ENUM_VALUE_TYPE(1)
VRState_Searching_Alert = ENUM_VALUE_TYPE(2)
VRState_Ready = ENUM_VALUE_TYPE(3)
VRState_Ready_Alert = ENUM_VALUE_TYPE(4)
VRState_NotReady = ENUM_VALUE_TYPE(5)
VRState_Standby = ENUM_VALUE_TYPE(6)
VRState_Ready_Alert_Low = ENUM_VALUE_TYPE(7)

EVREventType = ENUM_TYPE
VREvent_None = ENUM_VALUE_TYPE(0)
VREvent_TrackedDeviceActivated = ENUM_VALUE_TYPE(100)
VREvent_TrackedDeviceDeactivated = ENUM_VALUE_TYPE(101)
VREvent_TrackedDeviceUpdated = ENUM_VALUE_TYPE(102)
VREvent_TrackedDeviceUserInteractionStarted = ENUM_VALUE_TYPE(103)
VREvent_TrackedDeviceUserInteractionEnded = ENUM_VALUE_TYPE(104)
VREvent_IpdChanged = ENUM_VALUE_TYPE(105)
VREvent_EnterStandbyMode = ENUM_VALUE_TYPE(106)
VREvent_LeaveStandbyMode = ENUM_VALUE_TYPE(107)
VREvent_TrackedDeviceRoleChanged = ENUM_VALUE_TYPE(108)
VREvent_WatchdogWakeUpRequested = ENUM_VALUE_TYPE(109)
VREvent_LensDistortionChanged = ENUM_VALUE_TYPE(110)
VREvent_PropertyChanged = ENUM_VALUE_TYPE(111)
VREvent_ButtonPress = ENUM_VALUE_TYPE(200)
VREvent_ButtonUnpress = ENUM_VALUE_TYPE(201)
VREvent_ButtonTouch = ENUM_VALUE_TYPE(202)
VREvent_ButtonUntouch = ENUM_VALUE_TYPE(203)
VREvent_MouseMove = ENUM_VALUE_TYPE(300)
VREvent_MouseButtonDown = ENUM_VALUE_TYPE(301)
VREvent_MouseButtonUp = ENUM_VALUE_TYPE(302)
VREvent_FocusEnter = ENUM_VALUE_TYPE(303)
VREvent_FocusLeave = ENUM_VALUE_TYPE(304)
VREvent_Scroll = ENUM_VALUE_TYPE(305)
VREvent_TouchPadMove = ENUM_VALUE_TYPE(306)
VREvent_OverlayFocusChanged = ENUM_VALUE_TYPE(307)
VREvent_InputFocusCaptured = ENUM_VALUE_TYPE(400)
VREvent_InputFocusReleased = ENUM_VALUE_TYPE(401)
VREvent_SceneFocusLost = ENUM_VALUE_TYPE(402)
VREvent_SceneFocusGained = ENUM_VALUE_TYPE(403)
VREvent_SceneApplicationChanged = ENUM_VALUE_TYPE(404)
VREvent_SceneFocusChanged = ENUM_VALUE_TYPE(405)
VREvent_InputFocusChanged = ENUM_VALUE_TYPE(406)
VREvent_SceneApplicationSecondaryRenderingStarted = ENUM_VALUE_TYPE(407)
VREvent_HideRenderModels = ENUM_VALUE_TYPE(410)
VREvent_ShowRenderModels = ENUM_VALUE_TYPE(411)
VREvent_OverlayShown = ENUM_VALUE_TYPE(500)
VREvent_OverlayHidden = ENUM_VALUE_TYPE(501)
VREvent_DashboardActivated = ENUM_VALUE_TYPE(502)
VREvent_DashboardDeactivated = ENUM_VALUE_TYPE(503)
VREvent_DashboardThumbSelected = ENUM_VALUE_TYPE(504)
VREvent_DashboardRequested = ENUM_VALUE_TYPE(505)
VREvent_ResetDashboard = ENUM_VALUE_TYPE(506)
VREvent_RenderToast = ENUM_VALUE_TYPE(507)
VREvent_ImageLoaded = ENUM_VALUE_TYPE(508)
VREvent_ShowKeyboard = ENUM_VALUE_TYPE(509)
VREvent_HideKeyboard = ENUM_VALUE_TYPE(510)
VREvent_OverlayGamepadFocusGained = ENUM_VALUE_TYPE(511)
VREvent_OverlayGamepadFocusLost = ENUM_VALUE_TYPE(512)
VREvent_OverlaySharedTextureChanged = ENUM_VALUE_TYPE(513)
VREvent_DashboardGuideButtonDown = ENUM_VALUE_TYPE(514)
VREvent_DashboardGuideButtonUp = ENUM_VALUE_TYPE(515)
VREvent_ScreenshotTriggered = ENUM_VALUE_TYPE(516)
VREvent_ImageFailed = ENUM_VALUE_TYPE(517)
VREvent_DashboardOverlayCreated = ENUM_VALUE_TYPE(518)
VREvent_RequestScreenshot = ENUM_VALUE_TYPE(520)
VREvent_ScreenshotTaken = ENUM_VALUE_TYPE(521)
VREvent_ScreenshotFailed = ENUM_VALUE_TYPE(522)
VREvent_SubmitScreenshotToDashboard = ENUM_VALUE_TYPE(523)
VREvent_ScreenshotProgressToDashboard = ENUM_VALUE_TYPE(524)
VREvent_PrimaryDashboardDeviceChanged = ENUM_VALUE_TYPE(525)
VREvent_Notification_Shown = ENUM_VALUE_TYPE(600)
VREvent_Notification_Hidden = ENUM_VALUE_TYPE(601)
VREvent_Notification_BeginInteraction = ENUM_VALUE_TYPE(602)
VREvent_Notification_Destroyed = ENUM_VALUE_TYPE(603)
VREvent_Quit = ENUM_VALUE_TYPE(700)
VREvent_ProcessQuit = ENUM_VALUE_TYPE(701)
VREvent_QuitAborted_UserPrompt = ENUM_VALUE_TYPE(702)
VREvent_QuitAcknowledged = ENUM_VALUE_TYPE(703)
VREvent_DriverRequestedQuit = ENUM_VALUE_TYPE(704)
VREvent_ChaperoneDataHasChanged = ENUM_VALUE_TYPE(800)
VREvent_ChaperoneUniverseHasChanged = ENUM_VALUE_TYPE(801)
VREvent_ChaperoneTempDataHasChanged = ENUM_VALUE_TYPE(802)
VREvent_ChaperoneSettingsHaveChanged = ENUM_VALUE_TYPE(803)
VREvent_SeatedZeroPoseReset = ENUM_VALUE_TYPE(804)
VREvent_AudioSettingsHaveChanged = ENUM_VALUE_TYPE(820)
VREvent_BackgroundSettingHasChanged = ENUM_VALUE_TYPE(850)
VREvent_CameraSettingsHaveChanged = ENUM_VALUE_TYPE(851)
VREvent_ReprojectionSettingHasChanged = ENUM_VALUE_TYPE(852)
VREvent_ModelSkinSettingsHaveChanged = ENUM_VALUE_TYPE(853)
VREvent_EnvironmentSettingsHaveChanged = ENUM_VALUE_TYPE(854)
VREvent_PowerSettingsHaveChanged = ENUM_VALUE_TYPE(855)
VREvent_StatusUpdate = ENUM_VALUE_TYPE(900)
VREvent_MCImageUpdated = ENUM_VALUE_TYPE(1000)
VREvent_FirmwareUpdateStarted = ENUM_VALUE_TYPE(1100)
VREvent_FirmwareUpdateFinished = ENUM_VALUE_TYPE(1101)
VREvent_KeyboardClosed = ENUM_VALUE_TYPE(1200)
VREvent_KeyboardCharInput = ENUM_VALUE_TYPE(1201)
VREvent_KeyboardDone = ENUM_VALUE_TYPE(1202)
VREvent_ApplicationTransitionStarted = ENUM_VALUE_TYPE(1300)
VREvent_ApplicationTransitionAborted = ENUM_VALUE_TYPE(1301)
VREvent_ApplicationTransitionNewAppStarted = ENUM_VALUE_TYPE(1302)
VREvent_ApplicationListUpdated = ENUM_VALUE_TYPE(1303)
VREvent_ApplicationMimeTypeLoad = ENUM_VALUE_TYPE(1304)
VREvent_ApplicationTransitionNewAppLaunchComplete = ENUM_VALUE_TYPE(1305)
VREvent_ProcessConnected = ENUM_VALUE_TYPE(1306)
VREvent_ProcessDisconnected = ENUM_VALUE_TYPE(1307)
VREvent_Compositor_MirrorWindowShown = ENUM_VALUE_TYPE(1400)
VREvent_Compositor_MirrorWindowHidden = ENUM_VALUE_TYPE(1401)
VREvent_Compositor_ChaperoneBoundsShown = ENUM_VALUE_TYPE(1410)
VREvent_Compositor_ChaperoneBoundsHidden = ENUM_VALUE_TYPE(1411)
VREvent_TrackedCamera_StartVideoStream = ENUM_VALUE_TYPE(1500)
VREvent_TrackedCamera_StopVideoStream = ENUM_VALUE_TYPE(1501)
VREvent_TrackedCamera_PauseVideoStream = ENUM_VALUE_TYPE(1502)
VREvent_TrackedCamera_ResumeVideoStream = ENUM_VALUE_TYPE(1503)
VREvent_TrackedCamera_EditingSurface = ENUM_VALUE_TYPE(1550)
VREvent_PerformanceTest_EnableCapture = ENUM_VALUE_TYPE(1600)
VREvent_PerformanceTest_DisableCapture = ENUM_VALUE_TYPE(1601)
VREvent_PerformanceTest_FidelityLevel = ENUM_VALUE_TYPE(1602)
VREvent_MessageOverlay_Closed = ENUM_VALUE_TYPE(1650)
VREvent_VendorSpecific_Reserved_Start = ENUM_VALUE_TYPE(10000)
VREvent_VendorSpecific_Reserved_End = ENUM_VALUE_TYPE(19999)

EDeviceActivityLevel = ENUM_TYPE
k_EDeviceActivityLevel_Unknown = ENUM_VALUE_TYPE(-1)
k_EDeviceActivityLevel_Idle = ENUM_VALUE_TYPE(0)
k_EDeviceActivityLevel_UserInteraction = ENUM_VALUE_TYPE(1)
k_EDeviceActivityLevel_UserInteraction_Timeout = ENUM_VALUE_TYPE(2)
k_EDeviceActivityLevel_Standby = ENUM_VALUE_TYPE(3)

EVRButtonId = ENUM_TYPE
k_EButton_System = ENUM_VALUE_TYPE(0)
k_EButton_ApplicationMenu = ENUM_VALUE_TYPE(1)
k_EButton_Grip = ENUM_VALUE_TYPE(2)
k_EButton_DPad_Left = ENUM_VALUE_TYPE(3)
k_EButton_DPad_Up = ENUM_VALUE_TYPE(4)
k_EButton_DPad_Right = ENUM_VALUE_TYPE(5)
k_EButton_DPad_Down = ENUM_VALUE_TYPE(6)
k_EButton_A = ENUM_VALUE_TYPE(7)
k_EButton_ProximitySensor = ENUM_VALUE_TYPE(31)
k_EButton_Axis0 = ENUM_VALUE_TYPE(32)
k_EButton_Axis1 = ENUM_VALUE_TYPE(33)
k_EButton_Axis2 = ENUM_VALUE_TYPE(34)
k_EButton_Axis3 = ENUM_VALUE_TYPE(35)
k_EButton_Axis4 = ENUM_VALUE_TYPE(36)
k_EButton_SteamVR_Touchpad = ENUM_VALUE_TYPE(32)
k_EButton_SteamVR_Trigger = ENUM_VALUE_TYPE(33)
k_EButton_Dashboard_Back = ENUM_VALUE_TYPE(2)
k_EButton_Max = ENUM_VALUE_TYPE(64)

EVRMouseButton = ENUM_TYPE
VRMouseButton_Left = ENUM_VALUE_TYPE(1)
VRMouseButton_Right = ENUM_VALUE_TYPE(2)
VRMouseButton_Middle = ENUM_VALUE_TYPE(4)

EHiddenAreaMeshType = ENUM_TYPE
k_eHiddenAreaMesh_Standard = ENUM_VALUE_TYPE(0)
k_eHiddenAreaMesh_Inverse = ENUM_VALUE_TYPE(1)
k_eHiddenAreaMesh_LineLoop = ENUM_VALUE_TYPE(2)
k_eHiddenAreaMesh_Max = ENUM_VALUE_TYPE(3)

EVRControllerAxisType = ENUM_TYPE
k_eControllerAxis_None = ENUM_VALUE_TYPE(0)
k_eControllerAxis_TrackPad = ENUM_VALUE_TYPE(1)
k_eControllerAxis_Joystick = ENUM_VALUE_TYPE(2)
k_eControllerAxis_Trigger = ENUM_VALUE_TYPE(3)

EVRControllerEventOutputType = ENUM_TYPE
ControllerEventOutput_OSEvents = ENUM_VALUE_TYPE(0)
ControllerEventOutput_VREvents = ENUM_VALUE_TYPE(1)

ECollisionBoundsStyle = ENUM_TYPE
COLLISION_BOUNDS_STYLE_BEGINNER = ENUM_VALUE_TYPE(0)
COLLISION_BOUNDS_STYLE_INTERMEDIATE = ENUM_VALUE_TYPE(1)
COLLISION_BOUNDS_STYLE_SQUARES = ENUM_VALUE_TYPE(2)
COLLISION_BOUNDS_STYLE_ADVANCED = ENUM_VALUE_TYPE(3)
COLLISION_BOUNDS_STYLE_NONE = ENUM_VALUE_TYPE(4)
COLLISION_BOUNDS_STYLE_COUNT = ENUM_VALUE_TYPE(5)

EVROverlayError = ENUM_TYPE
VROverlayError_None = ENUM_VALUE_TYPE(0)
VROverlayError_UnknownOverlay = ENUM_VALUE_TYPE(10)
VROverlayError_InvalidHandle = ENUM_VALUE_TYPE(11)
VROverlayError_PermissionDenied = ENUM_VALUE_TYPE(12)
VROverlayError_OverlayLimitExceeded = ENUM_VALUE_TYPE(13)
VROverlayError_WrongVisibilityType = ENUM_VALUE_TYPE(14)
VROverlayError_KeyTooLong = ENUM_VALUE_TYPE(15)
VROverlayError_NameTooLong = ENUM_VALUE_TYPE(16)
VROverlayError_KeyInUse = ENUM_VALUE_TYPE(17)
VROverlayError_WrongTransformType = ENUM_VALUE_TYPE(18)
VROverlayError_InvalidTrackedDevice = ENUM_VALUE_TYPE(19)
VROverlayError_InvalidParameter = ENUM_VALUE_TYPE(20)
VROverlayError_ThumbnailCantBeDestroyed = ENUM_VALUE_TYPE(21)
VROverlayError_ArrayTooSmall = ENUM_VALUE_TYPE(22)
VROverlayError_RequestFailed = ENUM_VALUE_TYPE(23)
VROverlayError_InvalidTexture = ENUM_VALUE_TYPE(24)
VROverlayError_UnableToLoadFile = ENUM_VALUE_TYPE(25)
VROverlayError_KeyboardAlreadyInUse = ENUM_VALUE_TYPE(26)
VROverlayError_NoNeighbor = ENUM_VALUE_TYPE(27)
VROverlayError_TooManyMaskPrimitives = ENUM_VALUE_TYPE(29)
VROverlayError_BadMaskPrimitive = ENUM_VALUE_TYPE(30)

EVRApplicationType = ENUM_TYPE
VRApplication_Other = ENUM_VALUE_TYPE(0)
VRApplication_Scene = ENUM_VALUE_TYPE(1)
VRApplication_Overlay = ENUM_VALUE_TYPE(2)
VRApplication_Background = ENUM_VALUE_TYPE(3)
VRApplication_Utility = ENUM_VALUE_TYPE(4)
VRApplication_VRMonitor = ENUM_VALUE_TYPE(5)
VRApplication_SteamWatchdog = ENUM_VALUE_TYPE(6)
VRApplication_Bootstrapper = ENUM_VALUE_TYPE(7)
VRApplication_Max = ENUM_VALUE_TYPE(8)

EVRFirmwareError = ENUM_TYPE
VRFirmwareError_None = ENUM_VALUE_TYPE(0)
VRFirmwareError_Success = ENUM_VALUE_TYPE(1)
VRFirmwareError_Fail = ENUM_VALUE_TYPE(2)

EVRNotificationError = ENUM_TYPE
VRNotificationError_OK = ENUM_VALUE_TYPE(0)
VRNotificationError_InvalidNotificationId = ENUM_VALUE_TYPE(100)
VRNotificationError_NotificationQueueFull = ENUM_VALUE_TYPE(101)
VRNotificationError_InvalidOverlayHandle = ENUM_VALUE_TYPE(102)
VRNotificationError_SystemWithUserValueAlreadyExists = ENUM_VALUE_TYPE(103)

EVRInitError = ENUM_TYPE
VRInitError_None = ENUM_VALUE_TYPE(0)
VRInitError_Unknown = ENUM_VALUE_TYPE(1)
VRInitError_Init_InstallationNotFound = ENUM_VALUE_TYPE(100)
VRInitError_Init_InstallationCorrupt = ENUM_VALUE_TYPE(101)
VRInitError_Init_VRClientDLLNotFound = ENUM_VALUE_TYPE(102)
VRInitError_Init_FileNotFound = ENUM_VALUE_TYPE(103)
VRInitError_Init_FactoryNotFound = ENUM_VALUE_TYPE(104)
VRInitError_Init_InterfaceNotFound = ENUM_VALUE_TYPE(105)
VRInitError_Init_InvalidInterface = ENUM_VALUE_TYPE(106)
VRInitError_Init_UserConfigDirectoryInvalid = ENUM_VALUE_TYPE(107)
VRInitError_Init_HmdNotFound = ENUM_VALUE_TYPE(108)
VRInitError_Init_NotInitialized = ENUM_VALUE_TYPE(109)
VRInitError_Init_PathRegistryNotFound = ENUM_VALUE_TYPE(110)
VRInitError_Init_NoConfigPath = ENUM_VALUE_TYPE(111)
VRInitError_Init_NoLogPath = ENUM_VALUE_TYPE(112)
VRInitError_Init_PathRegistryNotWritable = ENUM_VALUE_TYPE(113)
VRInitError_Init_AppInfoInitFailed = ENUM_VALUE_TYPE(114)
VRInitError_Init_Retry = ENUM_VALUE_TYPE(115)
VRInitError_Init_InitCanceledByUser = ENUM_VALUE_TYPE(116)
VRInitError_Init_AnotherAppLaunching = ENUM_VALUE_TYPE(117)
VRInitError_Init_SettingsInitFailed = ENUM_VALUE_TYPE(118)
VRInitError_Init_ShuttingDown = ENUM_VALUE_TYPE(119)
VRInitError_Init_TooManyObjects = ENUM_VALUE_TYPE(120)
VRInitError_Init_NoServerForBackgroundApp = ENUM_VALUE_TYPE(121)
VRInitError_Init_NotSupportedWithCompositor = ENUM_VALUE_TYPE(122)
VRInitError_Init_NotAvailableToUtilityApps = ENUM_VALUE_TYPE(123)
VRInitError_Init_Internal = ENUM_VALUE_TYPE(124)
VRInitError_Init_HmdDriverIdIsNone = ENUM_VALUE_TYPE(125)
VRInitError_Init_HmdNotFoundPresenceFailed = ENUM_VALUE_TYPE(126)
VRInitError_Init_VRMonitorNotFound = ENUM_VALUE_TYPE(127)
VRInitError_Init_VRMonitorStartupFailed = ENUM_VALUE_TYPE(128)
VRInitError_Init_LowPowerWatchdogNotSupported = ENUM_VALUE_TYPE(129)
VRInitError_Init_InvalidApplicationType = ENUM_VALUE_TYPE(130)
VRInitError_Init_NotAvailableToWatchdogApps = ENUM_VALUE_TYPE(131)
VRInitError_Init_WatchdogDisabledInSettings = ENUM_VALUE_TYPE(132)
VRInitError_Init_VRDashboardNotFound = ENUM_VALUE_TYPE(133)
VRInitError_Init_VRDashboardStartupFailed = ENUM_VALUE_TYPE(134)
VRInitError_Driver_Failed = ENUM_VALUE_TYPE(200)
VRInitError_Driver_Unknown = ENUM_VALUE_TYPE(201)
VRInitError_Driver_HmdUnknown = ENUM_VALUE_TYPE(202)
VRInitError_Driver_NotLoaded = ENUM_VALUE_TYPE(203)
VRInitError_Driver_RuntimeOutOfDate = ENUM_VALUE_TYPE(204)
VRInitError_Driver_HmdInUse = ENUM_VALUE_TYPE(205)
VRInitError_Driver_NotCalibrated = ENUM_VALUE_TYPE(206)
VRInitError_Driver_CalibrationInvalid = ENUM_VALUE_TYPE(207)
VRInitError_Driver_HmdDisplayNotFound = ENUM_VALUE_TYPE(208)
VRInitError_Driver_TrackedDeviceInterfaceUnknown = ENUM_VALUE_TYPE(209)
VRInitError_Driver_HmdDriverIdOutOfBounds = ENUM_VALUE_TYPE(211)
VRInitError_Driver_HmdDisplayMirrored = ENUM_VALUE_TYPE(212)
VRInitError_IPC_ServerInitFailed = ENUM_VALUE_TYPE(300)
VRInitError_IPC_ConnectFailed = ENUM_VALUE_TYPE(301)
VRInitError_IPC_SharedStateInitFailed = ENUM_VALUE_TYPE(302)
VRInitError_IPC_CompositorInitFailed = ENUM_VALUE_TYPE(303)
VRInitError_IPC_MutexInitFailed = ENUM_VALUE_TYPE(304)
VRInitError_IPC_Failed = ENUM_VALUE_TYPE(305)
VRInitError_IPC_CompositorConnectFailed = ENUM_VALUE_TYPE(306)
VRInitError_IPC_CompositorInvalidConnectResponse = ENUM_VALUE_TYPE(307)
VRInitError_IPC_ConnectFailedAfterMultipleAttempts = ENUM_VALUE_TYPE(308)
VRInitError_Compositor_Failed = ENUM_VALUE_TYPE(400)
VRInitError_Compositor_D3D11HardwareRequired = ENUM_VALUE_TYPE(401)
VRInitError_Compositor_FirmwareRequiresUpdate = ENUM_VALUE_TYPE(402)
VRInitError_Compositor_OverlayInitFailed = ENUM_VALUE_TYPE(403)
VRInitError_Compositor_ScreenshotsInitFailed = ENUM_VALUE_TYPE(404)
VRInitError_VendorSpecific_UnableToConnectToOculusRuntime = ENUM_VALUE_TYPE(1000)
VRInitError_VendorSpecific_HmdFound_CantOpenDevice = ENUM_VALUE_TYPE(1101)
VRInitError_VendorSpecific_HmdFound_UnableToRequestConfigStart = ENUM_VALUE_TYPE(1102)
VRInitError_VendorSpecific_HmdFound_NoStoredConfig = ENUM_VALUE_TYPE(1103)
VRInitError_VendorSpecific_HmdFound_ConfigTooBig = ENUM_VALUE_TYPE(1104)
VRInitError_VendorSpecific_HmdFound_ConfigTooSmall = ENUM_VALUE_TYPE(1105)
VRInitError_VendorSpecific_HmdFound_UnableToInitZLib = ENUM_VALUE_TYPE(1106)
VRInitError_VendorSpecific_HmdFound_CantReadFirmwareVersion = ENUM_VALUE_TYPE(1107)
VRInitError_VendorSpecific_HmdFound_UnableToSendUserDataStart = ENUM_VALUE_TYPE(1108)
VRInitError_VendorSpecific_HmdFound_UnableToGetUserDataStart = ENUM_VALUE_TYPE(1109)
VRInitError_VendorSpecific_HmdFound_UnableToGetUserDataNext = ENUM_VALUE_TYPE(1110)
VRInitError_VendorSpecific_HmdFound_UserDataAddressRange = ENUM_VALUE_TYPE(1111)
VRInitError_VendorSpecific_HmdFound_UserDataError = ENUM_VALUE_TYPE(1112)
VRInitError_VendorSpecific_HmdFound_ConfigFailedSanityCheck = ENUM_VALUE_TYPE(1113)
VRInitError_Steam_SteamInstallationNotFound = ENUM_VALUE_TYPE(2000)

EVRScreenshotType = ENUM_TYPE
VRScreenshotType_None = ENUM_VALUE_TYPE(0)
VRScreenshotType_Mono = ENUM_VALUE_TYPE(1)
VRScreenshotType_Stereo = ENUM_VALUE_TYPE(2)
VRScreenshotType_Cubemap = ENUM_VALUE_TYPE(3)
VRScreenshotType_MonoPanorama = ENUM_VALUE_TYPE(4)
VRScreenshotType_StereoPanorama = ENUM_VALUE_TYPE(5)

EVRScreenshotPropertyFilenames = ENUM_TYPE
VRScreenshotPropertyFilenames_Preview = ENUM_VALUE_TYPE(0)
VRScreenshotPropertyFilenames_VR = ENUM_VALUE_TYPE(1)

EVRTrackedCameraError = ENUM_TYPE
VRTrackedCameraError_None = ENUM_VALUE_TYPE(0)
VRTrackedCameraError_OperationFailed = ENUM_VALUE_TYPE(100)
VRTrackedCameraError_InvalidHandle = ENUM_VALUE_TYPE(101)
VRTrackedCameraError_InvalidFrameHeaderVersion = ENUM_VALUE_TYPE(102)
VRTrackedCameraError_OutOfHandles = ENUM_VALUE_TYPE(103)
VRTrackedCameraError_IPCFailure = ENUM_VALUE_TYPE(104)
VRTrackedCameraError_NotSupportedForThisDevice = ENUM_VALUE_TYPE(105)
VRTrackedCameraError_SharedMemoryFailure = ENUM_VALUE_TYPE(106)
VRTrackedCameraError_FrameBufferingFailure = ENUM_VALUE_TYPE(107)
VRTrackedCameraError_StreamSetupFailure = ENUM_VALUE_TYPE(108)
VRTrackedCameraError_InvalidGLTextureId = ENUM_VALUE_TYPE(109)
VRTrackedCameraError_InvalidSharedTextureHandle = ENUM_VALUE_TYPE(110)
VRTrackedCameraError_FailedToGetGLTextureId = ENUM_VALUE_TYPE(111)
VRTrackedCameraError_SharedTextureFailure = ENUM_VALUE_TYPE(112)
VRTrackedCameraError_NoFrameAvailable = ENUM_VALUE_TYPE(113)
VRTrackedCameraError_InvalidArgument = ENUM_VALUE_TYPE(114)
VRTrackedCameraError_InvalidFrameBufferSize = ENUM_VALUE_TYPE(115)

EVRTrackedCameraFrameType = ENUM_TYPE
VRTrackedCameraFrameType_Distorted = ENUM_VALUE_TYPE(0)
VRTrackedCameraFrameType_Undistorted = ENUM_VALUE_TYPE(1)
VRTrackedCameraFrameType_MaximumUndistorted = ENUM_VALUE_TYPE(2)
MAX_CAMERA_FRAME_TYPES = ENUM_VALUE_TYPE(3)

EVRApplicationError = ENUM_TYPE
VRApplicationError_None = ENUM_VALUE_TYPE(0)
VRApplicationError_AppKeyAlreadyExists = ENUM_VALUE_TYPE(100)
VRApplicationError_NoManifest = ENUM_VALUE_TYPE(101)
VRApplicationError_NoApplication = ENUM_VALUE_TYPE(102)
VRApplicationError_InvalidIndex = ENUM_VALUE_TYPE(103)
VRApplicationError_UnknownApplication = ENUM_VALUE_TYPE(104)
VRApplicationError_IPCFailed = ENUM_VALUE_TYPE(105)
VRApplicationError_ApplicationAlreadyRunning = ENUM_VALUE_TYPE(106)
VRApplicationError_InvalidManifest = ENUM_VALUE_TYPE(107)
VRApplicationError_InvalidApplication = ENUM_VALUE_TYPE(108)
VRApplicationError_LaunchFailed = ENUM_VALUE_TYPE(109)
VRApplicationError_ApplicationAlreadyStarting = ENUM_VALUE_TYPE(110)
VRApplicationError_LaunchInProgress = ENUM_VALUE_TYPE(111)
VRApplicationError_OldApplicationQuitting = ENUM_VALUE_TYPE(112)
VRApplicationError_TransitionAborted = ENUM_VALUE_TYPE(113)
VRApplicationError_IsTemplate = ENUM_VALUE_TYPE(114)
VRApplicationError_BufferTooSmall = ENUM_VALUE_TYPE(200)
VRApplicationError_PropertyNotSet = ENUM_VALUE_TYPE(201)
VRApplicationError_UnknownProperty = ENUM_VALUE_TYPE(202)
VRApplicationError_InvalidParameter = ENUM_VALUE_TYPE(203)

EVRApplicationProperty = ENUM_TYPE
VRApplicationProperty_Name_String = ENUM_VALUE_TYPE(0)
VRApplicationProperty_LaunchType_String = ENUM_VALUE_TYPE(11)
VRApplicationProperty_WorkingDirectory_String = ENUM_VALUE_TYPE(12)
VRApplicationProperty_BinaryPath_String = ENUM_VALUE_TYPE(13)
VRApplicationProperty_Arguments_String = ENUM_VALUE_TYPE(14)
VRApplicationProperty_URL_String = ENUM_VALUE_TYPE(15)
VRApplicationProperty_Description_String = ENUM_VALUE_TYPE(50)
VRApplicationProperty_NewsURL_String = ENUM_VALUE_TYPE(51)
VRApplicationProperty_ImagePath_String = ENUM_VALUE_TYPE(52)
VRApplicationProperty_Source_String = ENUM_VALUE_TYPE(53)
VRApplicationProperty_IsDashboardOverlay_Bool = ENUM_VALUE_TYPE(60)
VRApplicationProperty_IsTemplate_Bool = ENUM_VALUE_TYPE(61)
VRApplicationProperty_IsInstanced_Bool = ENUM_VALUE_TYPE(62)
VRApplicationProperty_IsInternal_Bool = ENUM_VALUE_TYPE(63)
VRApplicationProperty_LastLaunchTime_Uint64 = ENUM_VALUE_TYPE(70)

EVRApplicationTransitionState = ENUM_TYPE
VRApplicationTransition_None = ENUM_VALUE_TYPE(0)
VRApplicationTransition_OldAppQuitSent = ENUM_VALUE_TYPE(10)
VRApplicationTransition_WaitingForExternalLaunch = ENUM_VALUE_TYPE(11)
VRApplicationTransition_NewAppLaunched = ENUM_VALUE_TYPE(20)

ChaperoneCalibrationState = ENUM_TYPE
ChaperoneCalibrationState_OK = ENUM_VALUE_TYPE(1)
ChaperoneCalibrationState_Warning = ENUM_VALUE_TYPE(100)
ChaperoneCalibrationState_Warning_BaseStationMayHaveMoved = ENUM_VALUE_TYPE(101)
ChaperoneCalibrationState_Warning_BaseStationRemoved = ENUM_VALUE_TYPE(102)
ChaperoneCalibrationState_Warning_SeatedBoundsInvalid = ENUM_VALUE_TYPE(103)
ChaperoneCalibrationState_Error = ENUM_VALUE_TYPE(200)
ChaperoneCalibrationState_Error_BaseStationUninitialized = ENUM_VALUE_TYPE(201)
ChaperoneCalibrationState_Error_BaseStationConflict = ENUM_VALUE_TYPE(202)
ChaperoneCalibrationState_Error_PlayAreaInvalid = ENUM_VALUE_TYPE(203)
ChaperoneCalibrationState_Error_CollisionBoundsInvalid = ENUM_VALUE_TYPE(204)

EChaperoneConfigFile = ENUM_TYPE
EChaperoneConfigFile_Live = ENUM_VALUE_TYPE(1)
EChaperoneConfigFile_Temp = ENUM_VALUE_TYPE(2)

EChaperoneImportFlags = ENUM_TYPE
EChaperoneImport_BoundsOnly = ENUM_VALUE_TYPE(1)

EVRCompositorError = ENUM_TYPE
VRCompositorError_None = ENUM_VALUE_TYPE(0)
VRCompositorError_RequestFailed = ENUM_VALUE_TYPE(1)
VRCompositorError_IncompatibleVersion = ENUM_VALUE_TYPE(100)
VRCompositorError_DoNotHaveFocus = ENUM_VALUE_TYPE(101)
VRCompositorError_InvalidTexture = ENUM_VALUE_TYPE(102)
VRCompositorError_IsNotSceneApplication = ENUM_VALUE_TYPE(103)
VRCompositorError_TextureIsOnWrongDevice = ENUM_VALUE_TYPE(104)
VRCompositorError_TextureUsesUnsupportedFormat = ENUM_VALUE_TYPE(105)
VRCompositorError_SharedTexturesNotSupported = ENUM_VALUE_TYPE(106)
VRCompositorError_IndexOutOfRange = ENUM_VALUE_TYPE(107)
VRCompositorError_AlreadySubmitted = ENUM_VALUE_TYPE(108)

VROverlayInputMethod = ENUM_TYPE
VROverlayInputMethod_None = ENUM_VALUE_TYPE(0)
VROverlayInputMethod_Mouse = ENUM_VALUE_TYPE(1)

VROverlayTransformType = ENUM_TYPE
VROverlayTransform_Absolute = ENUM_VALUE_TYPE(0)
VROverlayTransform_TrackedDeviceRelative = ENUM_VALUE_TYPE(1)
VROverlayTransform_SystemOverlay = ENUM_VALUE_TYPE(2)
VROverlayTransform_TrackedComponent = ENUM_VALUE_TYPE(3)

VROverlayFlags = ENUM_TYPE
VROverlayFlags_None = ENUM_VALUE_TYPE(0)
VROverlayFlags_Curved = ENUM_VALUE_TYPE(1)
VROverlayFlags_RGSS4X = ENUM_VALUE_TYPE(2)
VROverlayFlags_NoDashboardTab = ENUM_VALUE_TYPE(3)
VROverlayFlags_AcceptsGamepadEvents = ENUM_VALUE_TYPE(4)
VROverlayFlags_ShowGamepadFocus = ENUM_VALUE_TYPE(5)
VROverlayFlags_SendVRScrollEvents = ENUM_VALUE_TYPE(6)
VROverlayFlags_SendVRTouchpadEvents = ENUM_VALUE_TYPE(7)
VROverlayFlags_ShowTouchPadScrollWheel = ENUM_VALUE_TYPE(8)
VROverlayFlags_TransferOwnershipToInternalProcess = ENUM_VALUE_TYPE(9)
VROverlayFlags_SideBySide_Parallel = ENUM_VALUE_TYPE(10)
VROverlayFlags_SideBySide_Crossed = ENUM_VALUE_TYPE(11)
VROverlayFlags_Panorama = ENUM_VALUE_TYPE(12)
VROverlayFlags_StereoPanorama = ENUM_VALUE_TYPE(13)
VROverlayFlags_SortWithNonSceneOverlays = ENUM_VALUE_TYPE(14)
VROverlayFlags_VisibleInDashboard = ENUM_VALUE_TYPE(15)

VRMessageOverlayResponse = ENUM_TYPE
ButtonPress_0 = ENUM_VALUE_TYPE(0)
ButtonPress_1 = ENUM_VALUE_TYPE(1)
ButtonPress_2 = ENUM_VALUE_TYPE(2)
ButtonPress_3 = ENUM_VALUE_TYPE(3)
CouldntFindSystemOverlay = ENUM_VALUE_TYPE(4)
CouldntFindOrCreateClientOverlay = ENUM_VALUE_TYPE(5)
ApplicationQuit = ENUM_VALUE_TYPE(6)

EGamepadTextInputMode = ENUM_TYPE
k_EGamepadTextInputModeNormal = ENUM_VALUE_TYPE(0)
k_EGamepadTextInputModePassword = ENUM_VALUE_TYPE(1)
k_EGamepadTextInputModeSubmit = ENUM_VALUE_TYPE(2)

EGamepadTextInputLineMode = ENUM_TYPE
k_EGamepadTextInputLineModeSingleLine = ENUM_VALUE_TYPE(0)
k_EGamepadTextInputLineModeMultipleLines = ENUM_VALUE_TYPE(1)

EOverlayDirection = ENUM_TYPE
OverlayDirection_Up = ENUM_VALUE_TYPE(0)
OverlayDirection_Down = ENUM_VALUE_TYPE(1)
OverlayDirection_Left = ENUM_VALUE_TYPE(2)
OverlayDirection_Right = ENUM_VALUE_TYPE(3)
OverlayDirection_Count = ENUM_VALUE_TYPE(4)

EVROverlayIntersectionMaskPrimitiveType = ENUM_TYPE
OverlayIntersectionPrimitiveType_Rectangle = ENUM_VALUE_TYPE(0)
OverlayIntersectionPrimitiveType_Circle = ENUM_VALUE_TYPE(1)

EVRRenderModelError = ENUM_TYPE
VRRenderModelError_None = ENUM_VALUE_TYPE(0)
VRRenderModelError_Loading = ENUM_VALUE_TYPE(100)
VRRenderModelError_NotSupported = ENUM_VALUE_TYPE(200)
VRRenderModelError_InvalidArg = ENUM_VALUE_TYPE(300)
VRRenderModelError_InvalidModel = ENUM_VALUE_TYPE(301)
VRRenderModelError_NoShapes = ENUM_VALUE_TYPE(302)
VRRenderModelError_MultipleShapes = ENUM_VALUE_TYPE(303)
VRRenderModelError_TooManyVertices = ENUM_VALUE_TYPE(304)
VRRenderModelError_MultipleTextures = ENUM_VALUE_TYPE(305)
VRRenderModelError_BufferTooSmall = ENUM_VALUE_TYPE(306)
VRRenderModelError_NotEnoughNormals = ENUM_VALUE_TYPE(307)
VRRenderModelError_NotEnoughTexCoords = ENUM_VALUE_TYPE(308)
VRRenderModelError_InvalidTexture = ENUM_VALUE_TYPE(400)

EVRComponentProperty = ENUM_TYPE
VRComponentProperty_IsStatic = ENUM_VALUE_TYPE(1)
VRComponentProperty_IsVisible = ENUM_VALUE_TYPE(2)
VRComponentProperty_IsTouched = ENUM_VALUE_TYPE(4)
VRComponentProperty_IsPressed = ENUM_VALUE_TYPE(8)
VRComponentProperty_IsScrolled = ENUM_VALUE_TYPE(16)

EVRNotificationType = ENUM_TYPE
Transient = ENUM_VALUE_TYPE(0)
Persistent = ENUM_VALUE_TYPE(1)
Transient_SystemWithUserValue = ENUM_VALUE_TYPE(2)

EVRNotificationStyle = ENUM_TYPE
EVRNotificationStyle_None = ENUM_VALUE_TYPE(0)
EVRNotificationStyle_Application = ENUM_VALUE_TYPE(100)
EVRNotificationStyle_Contact_Disabled = ENUM_VALUE_TYPE(200)
EVRNotificationStyle_Contact_Enabled = ENUM_VALUE_TYPE(201)
EVRNotificationStyle_Contact_Active = ENUM_VALUE_TYPE(202)

EVRSettingsError = ENUM_TYPE
VRSettingsError_None = ENUM_VALUE_TYPE(0)
VRSettingsError_IPCFailed = ENUM_VALUE_TYPE(1)
VRSettingsError_WriteFailed = ENUM_VALUE_TYPE(2)
VRSettingsError_ReadFailed = ENUM_VALUE_TYPE(3)
VRSettingsError_JsonParseFailed = ENUM_VALUE_TYPE(4)
VRSettingsError_UnsetSettingHasNoDefault = ENUM_VALUE_TYPE(5)

EVRScreenshotError = ENUM_TYPE
VRScreenshotError_None = ENUM_VALUE_TYPE(0)
VRScreenshotError_RequestFailed = ENUM_VALUE_TYPE(1)
VRScreenshotError_IncompatibleVersion = ENUM_VALUE_TYPE(100)
VRScreenshotError_NotFound = ENUM_VALUE_TYPE(101)
VRScreenshotError_BufferTooSmall = ENUM_VALUE_TYPE(102)
VRScreenshotError_ScreenshotAlreadyInProgress = ENUM_VALUE_TYPE(108)


#######################
### Expose Typedefs ###
#######################

# Use c_ubyte instead of c_char, for better compatibility with Python True/False
openvr_bool = c_ubyte

PropertyContainerHandle_t = c_uint64
PropertyTypeTag_t = c_uint32
TrackedDeviceIndex_t = c_uint32
VRNotificationId = c_uint32
VROverlayHandle_t = c_uint64
glSharedTextureHandle_t = c_void_p
glInt_t = c_int32
glUInt_t = c_uint32
SharedTextureHandle_t = c_uint64
TrackedDeviceIndex_t = c_uint32
PropertyContainerHandle_t = c_uint64
PropertyTypeTag_t = c_uint32
VROverlayHandle_t = c_uint64
TrackedCameraHandle_t = c_uint64
ScreenshotHandle_t = c_uint32
VRComponentProperties = c_uint32
TextureID_t = c_int32
VRNotificationId = c_uint32
HmdError = EVRInitError
Hmd_Eye = EVREye
ColorSpace = EColorSpace
HmdTrackingResult = ETrackingResult
TrackedDeviceClass = ETrackedDeviceClass
TrackingUniverseOrigin = ETrackingUniverseOrigin
TrackedDeviceProperty = ETrackedDeviceProperty
TrackedPropertyError = ETrackedPropertyError
VRSubmitFlags_t = EVRSubmitFlags
VRState_t = EVRState
CollisionBoundsStyle_t = ECollisionBoundsStyle
VROverlayError = EVROverlayError
VRFirmwareError = EVRFirmwareError
VRCompositorError = EVRCompositorError
VRScreenshotsError = EVRScreenshotError

######################
### Expose classes ###
######################

class OpenVRError(RuntimeError):
    """
    OpenVRError is a custom exception type for when OpenVR functions return a failure code.
    Such a specific exception type allows more precise exception handling that does just raising Exception().
    """
    pass


# Methods to include in all openvr vector classes
class _VectorMixin(object):
    def __init__(self, *args):
        self._setArray(self._getArray().__class__(*args))

    def _getArray(self):
        return self.v

    def _setArray(self, array):
        self.v[:] = array[:]

    def __getitem__(self, key):
        return self._getArray()[key]

    def __len__(self):
        return len(self._getArray())

    def __setitem__(self, key, value):
        self._getArray()[key] = value

    def __str__(self):
        return str(list(self))


class _MatrixMixin(_VectorMixin):
    def _getArray(self):
        return self.m

    def _setArray(self, array):
        self.m[:] = array[:]

    def __str__(self):
        return str(list(list(e) for e in self))


class HmdMatrix34_t(_MatrixMixin, Structure):
    """
    right-handed system
    +y is up
    +x is to the right
    -z is going away from you
    Distance unit is  meters
    """

    _fields_ = [
        ("m", (c_float * 4) * 3),
    ]


class HmdMatrix44_t(_MatrixMixin, Structure):
    _fields_ = [
        ("m", (c_float * 4) * 4),
    ]


class HmdVector3_t(_VectorMixin, Structure):
    _fields_ = [
        ("v", c_float * 3),
    ]


class HmdVector4_t(_VectorMixin, Structure):
    _fields_ = [
        ("v", c_float * 4),
    ]


class HmdVector3d_t(_VectorMixin, Structure):
    _fields_ = [
        ("v", c_double * 3),
    ]


class HmdVector2_t(_VectorMixin, Structure):
    _fields_ = [
        ("v", c_float * 2),
    ]


class HmdQuaternion_t(Structure):
    _fields_ = [
        ("w", c_double),
        ("x", c_double),
        ("y", c_double),
        ("z", c_double),
    ]


class HmdColor_t(Structure):
    _fields_ = [
        ("r", c_float),
        ("g", c_float),
        ("b", c_float),
        ("a", c_float),
    ]


class HmdQuad_t(Structure):
    _fields_ = [
        ("vCorners", HmdVector3_t * 4),
    ]


class HmdRect2_t(Structure):
    _fields_ = [
        ("vTopLeft", HmdVector2_t),
        ("vBottomRight", HmdVector2_t),
    ]


class DistortionCoordinates_t(Structure):
    """
    Used to return the post-distortion UVs for each color channel. 
    UVs range from 0 to 1 with 0,0 in the upper left corner of the 
    source render target. The 0,0 to 1,1 range covers a single eye.
    """

    _fields_ = [
        ("rfRed", c_float * 2),
        ("rfGreen", c_float * 2),
        ("rfBlue", c_float * 2),
    ]


class Texture_t(Structure):
    _fields_ = [
        ("handle", c_void_p),
        ("eType", ETextureType),
        ("eColorSpace", EColorSpace),
    ]


class TrackedDevicePose_t(Structure):
    "describes a single pose for a tracked object"

    _fields_ = [
        ("mDeviceToAbsoluteTracking", HmdMatrix34_t),
        ("vVelocity", HmdVector3_t),
        ("vAngularVelocity", HmdVector3_t),
        ("eTrackingResult", ETrackingResult),
        ("bPoseIsValid", openvr_bool),
        ("bDeviceIsConnected", openvr_bool),
    ]


class VRTextureBounds_t(Structure):
    """
    Allows the application to control what part of the provided texture will be used in the
    frame buffer.
    """

    _fields_ = [
        ("uMin", c_float),
        ("vMin", c_float),
        ("uMax", c_float),
        ("vMax", c_float),
    ]


class VRVulkanTextureData_t(Structure):
    """
    Data required for passing Vulkan textures to IVRCompositor::Submit.
    Be sure to call OpenVR_Shutdown before destroying these resources.
    """

    _fields_ = [
        ("m_nImage", c_uint64),
        ("m_pDevice", POINTER(VkDevice_T)),
        ("m_pPhysicalDevice", POINTER(VkPhysicalDevice_T)),
        ("m_pInstance", POINTER(VkInstance_T)),
        ("m_pQueue", POINTER(VkQueue_T)),
        ("m_nQueueFamilyIndex", c_uint32),
        ("m_nWidth", c_uint32),
        ("m_nHeight", c_uint32),
        ("m_nFormat", c_uint32),
        ("m_nSampleCount", c_uint32),
    ]


class D3D12TextureData_t(Structure):
    """
    Data required for passing D3D12 textures to IVRCompositor::Submit.
    Be sure to call OpenVR_Shutdown before destroying these resources.
    """

    _fields_ = [
        ("m_pResource", POINTER(ID3D12Resource)),
        ("m_pCommandQueue", POINTER(ID3D12CommandQueue)),
        ("m_nNodeMask", c_uint32),
    ]


class VREvent_Controller_t(Structure):
    "used for controller button events"

    _fields_ = [
        ("button", c_uint32),
    ]


class VREvent_Mouse_t(Structure):
    "used for simulated mouse events in overlay space"

    _fields_ = [
        ("x", c_float),
        ("y", c_float),
        ("button", c_uint32),
    ]


class VREvent_Scroll_t(Structure):
    "used for simulated mouse wheel scroll in overlay space"

    _fields_ = [
        ("xdelta", c_float),
        ("ydelta", c_float),
        ("repeatCount", c_uint32),
    ]


class VREvent_TouchPadMove_t(Structure):
    """
    when in mouse input mode you can receive data from the touchpad, these events are only sent if the users finger
    is on the touchpad (or just released from it)
    """

    _fields_ = [
        ("bFingerDown", openvr_bool),
        ("flSecondsFingerDown", c_float),
        ("fValueXFirst", c_float),
        ("fValueYFirst", c_float),
        ("fValueXRaw", c_float),
        ("fValueYRaw", c_float),
    ]


class VREvent_Notification_t(Structure):
    "notification related events. Details will still change at this point"

    _fields_ = [
        ("ulUserValue", c_uint64),
        ("notificationId", c_uint32),
    ]


class VREvent_Process_t(Structure):
    "Used for events about processes"

    _fields_ = [
        ("pid", c_uint32),
        ("oldPid", c_uint32),
        ("bForced", openvr_bool),
    ]


class VREvent_Overlay_t(Structure):
    "Used for a few events about overlays"

    _fields_ = [
        ("overlayHandle", c_uint64),
    ]


class VREvent_Status_t(Structure):
    "Used for a few events about overlays"

    _fields_ = [
        ("statusState", c_uint32),
    ]


class VREvent_Keyboard_t(Structure):
    "Used for keyboard events"

    _fields_ = [
        ("cNewInput", c_char_p * 8),
        ("uUserValue", c_uint64),
    ]


class VREvent_Ipd_t(Structure):
    _fields_ = [
        ("ipdMeters", c_float),
    ]


class VREvent_Chaperone_t(Structure):
    _fields_ = [
        ("m_nPreviousUniverse", c_uint64),
        ("m_nCurrentUniverse", c_uint64),
    ]


class VREvent_Reserved_t(Structure):
    "Not actually used for any events"

    _fields_ = [
        ("reserved0", c_uint64),
        ("reserved1", c_uint64),
    ]


class VREvent_PerformanceTest_t(Structure):
    _fields_ = [
        ("m_nFidelityLevel", c_uint32),
    ]


class VREvent_SeatedZeroPoseReset_t(Structure):
    _fields_ = [
        ("bResetBySystemMenu", openvr_bool),
    ]


class VREvent_Screenshot_t(Structure):
    _fields_ = [
        ("handle", c_uint32),
        ("type", c_uint32),
    ]


class VREvent_ScreenshotProgress_t(Structure):
    _fields_ = [
        ("progress", c_float),
    ]


class VREvent_ApplicationLaunch_t(Structure):
    _fields_ = [
        ("pid", c_uint32),
        ("unArgsHandle", c_uint32),
    ]


class VREvent_EditingCameraSurface_t(Structure):
    _fields_ = [
        ("overlayHandle", c_uint64),
        ("nVisualMode", c_uint32),
    ]


class VREvent_MessageOverlay_t(Structure):
    _fields_ = [
        ("unVRMessageOverlayResponse", c_uint32),
    ]


class VREvent_Property_t(Structure):
    _fields_ = [
        ("container", PropertyContainerHandle_t),
        ("prop", ETrackedDeviceProperty),
    ]


class HiddenAreaMesh_t(Structure):
    """
    The mesh to draw into the stencil (or depth) buffer to perform 
    early stencil (or depth) kills of pixels that will never appear on the HMD.
    This mesh draws on all the pixels that will be hidden after distortion. 
    * If the HMD does not provide a visible area mesh pVertexData will be
    NULL and unTriangleCount will be 0.
    """

    _fields_ = [
        ("pVertexData", POINTER(HmdVector2_t)),
        ("unTriangleCount", c_uint32),
    ]


class VRControllerAxis_t(Structure):
    "contains information about one axis on the controller"

    _fields_ = [
        ("x", c_float),
        ("y", c_float),
    ]


class VRControllerState_t(Structure):
    _fields_ = [
        ("unPacketNum", c_uint32),
        ("ulButtonPressed", c_uint64),
        ("ulButtonTouched", c_uint64),
        ("rAxis", VRControllerAxis_t * 5),
    ]


class Compositor_OverlaySettings(Structure):
    "Allows the application to customize how the overlay appears in the compositor"

    _fields_ = [
        ("size", c_uint32),
        ("curved", openvr_bool),
        ("antialias", openvr_bool),
        ("scale", c_float),
        ("distance", c_float),
        ("alpha", c_float),
        ("uOffset", c_float),
        ("vOffset", c_float),
        ("uScale", c_float),
        ("vScale", c_float),
        ("gridDivs", c_float),
        ("gridWidth", c_float),
        ("gridScale", c_float),
        ("transform", HmdMatrix44_t),
    ]


class CameraVideoStreamFrameHeader_t(Structure):
    _fields_ = [
        ("eFrameType", EVRTrackedCameraFrameType),
        ("nWidth", c_uint32),
        ("nHeight", c_uint32),
        ("nBytesPerPixel", c_uint32),
        ("nFrameSequence", c_uint32),
        ("standingTrackedDevicePose", TrackedDevicePose_t),
    ]


class AppOverrideKeys_t(Structure):
    _fields_ = [
        ("pchKey", c_char_p),
        ("pchValue", c_char_p),
    ]


class Compositor_FrameTiming(Structure):
    "Provides a single frame's timing information to the app"

    _fields_ = [
        ("m_nSize", c_uint32),
        ("m_nFrameIndex", c_uint32),
        ("m_nNumFramePresents", c_uint32),
        ("m_nNumMisPresented", c_uint32),
        ("m_nNumDroppedFrames", c_uint32),
        ("m_nReprojectionFlags", c_uint32),
        ("m_flSystemTimeInSeconds", c_double),
        ("m_flPreSubmitGpuMs", c_float),
        ("m_flPostSubmitGpuMs", c_float),
        ("m_flTotalRenderGpuMs", c_float),
        ("m_flCompositorRenderGpuMs", c_float),
        ("m_flCompositorRenderCpuMs", c_float),
        ("m_flCompositorIdleCpuMs", c_float),
        ("m_flClientFrameIntervalMs", c_float),
        ("m_flPresentCallCpuMs", c_float),
        ("m_flWaitForPresentCpuMs", c_float),
        ("m_flSubmitFrameMs", c_float),
        ("m_flWaitGetPosesCalledMs", c_float),
        ("m_flNewPosesReadyMs", c_float),
        ("m_flNewFrameReadyMs", c_float),
        ("m_flCompositorUpdateStartMs", c_float),
        ("m_flCompositorUpdateEndMs", c_float),
        ("m_flCompositorRenderStartMs", c_float),
        ("m_HmdPose", TrackedDevicePose_t),
    ]


class Compositor_CumulativeStats(Structure):
    """
    Cumulative stats for current application.  These are not cleared until a new app connects,
    but they do stop accumulating once the associated app disconnects.
    """

    _fields_ = [
        ("m_nPid", c_uint32),
        ("m_nNumFramePresents", c_uint32),
        ("m_nNumDroppedFrames", c_uint32),
        ("m_nNumReprojectedFrames", c_uint32),
        ("m_nNumFramePresentsOnStartup", c_uint32),
        ("m_nNumDroppedFramesOnStartup", c_uint32),
        ("m_nNumReprojectedFramesOnStartup", c_uint32),
        ("m_nNumLoading", c_uint32),
        ("m_nNumFramePresentsLoading", c_uint32),
        ("m_nNumDroppedFramesLoading", c_uint32),
        ("m_nNumReprojectedFramesLoading", c_uint32),
        ("m_nNumTimedOut", c_uint32),
        ("m_nNumFramePresentsTimedOut", c_uint32),
        ("m_nNumDroppedFramesTimedOut", c_uint32),
        ("m_nNumReprojectedFramesTimedOut", c_uint32),
    ]


class VROverlayIntersectionParams_t(Structure):
    _fields_ = [
        ("vSource", HmdVector3_t),
        ("vDirection", HmdVector3_t),
        ("eOrigin", ETrackingUniverseOrigin),
    ]


class VROverlayIntersectionResults_t(Structure):
    _fields_ = [
        ("vPoint", HmdVector3_t),
        ("vNormal", HmdVector3_t),
        ("vUVs", HmdVector2_t),
        ("fDistance", c_float),
    ]


class IntersectionMaskRectangle_t(Structure):
    _fields_ = [
        ("m_flTopLeftX", c_float),
        ("m_flTopLeftY", c_float),
        ("m_flWidth", c_float),
        ("m_flHeight", c_float),
    ]


class IntersectionMaskCircle_t(Structure):
    _fields_ = [
        ("m_flCenterX", c_float),
        ("m_flCenterY", c_float),
        ("m_flRadius", c_float),
    ]


class RenderModel_ComponentState_t(Structure):
    "Describes state information about a render-model component, including transforms and other dynamic properties"

    _fields_ = [
        ("mTrackingToComponentRenderModel", HmdMatrix34_t),
        ("mTrackingToComponentLocal", HmdMatrix34_t),
        ("uProperties", VRComponentProperties),
    ]


class RenderModel_Vertex_t(Structure):
    "A single vertex in a render model"

    _fields_ = [
        ("vPosition", HmdVector3_t),
        ("vNormal", HmdVector3_t),
        ("rfTextureCoord", c_float * 2),
    ]


class RenderModel_TextureMap_t(Structure):
    _fields_ = [
        ("unWidth", c_uint16),
        ("unHeight", c_uint16),
        ("rubTextureMapData", POINTER(c_uint8)),
    ]


class RenderModel_t(Structure):
    _fields_ = [
        ("rVertexData", POINTER(RenderModel_Vertex_t)),
        ("unVertexCount", c_uint32),
        ("rIndexData", POINTER(c_uint16)),
        ("unTriangleCount", c_uint32),
        ("diffuseTextureId", TextureID_t),
    ]


class RenderModel_ControllerMode_State_t(Structure):
    _fields_ = [
        ("bScrollWheelVisible", openvr_bool),
    ]


class NotificationBitmap_t(Structure):
    "Used for passing graphic data"

    _fields_ = [
        ("m_pImageData", c_void_p),
        ("m_nWidth", c_int32),
        ("m_nHeight", c_int32),
        ("m_nBytesPerPixel", c_int32),
    ]


class COpenVRContext(object):
    def __init__(self):
        self.clear()
        
    def checkClear(self):
        global _vr_token
        if _vr_token != getInitToken():
            self.clear()
            _vr_token = getInitToken()
            
    def clear(self):  
        self.m_pVRSystem = None
        self.m_pVRChaperone = None
        self.m_pVRChaperoneSetup = None
        self.m_pVRCompositor = None
        self.m_pVROverlay = None
        self.m_pVRResources = None
        self.m_pVRRenderModels = None
        self.m_pVRExtendedDisplay = None
        self.m_pVRSettings = None
        self.m_pVRApplications = None
        self.m_pVRTrackedCamera = None
        self.m_pVRScreenshots = None

    def VRSystem(self):
        self.checkClear()
        if self.m_pVRSystem is None:
            self.m_pVRSystem = IVRSystem()
        return self.m_pVRSystem

    def VRChaperone(self):
        self.checkClear()
        if self.m_pVRChaperone is None:
            self.m_pVRChaperone = IVRChaperone()
        return self.m_pVRChaperone

    def VRChaperoneSetup(self):
        self.checkClear()
        if self.m_pVRChaperoneSetup is None:
            self.m_pVRChaperoneSetup = IVRChaperoneSetup()
        return self.m_pVRChaperoneSetup

    def VRCompositor(self):
        self.checkClear()
        if self.m_pVRCompositor is None:
            self.m_pVRCompositor = IVRCompositor()
        return self.m_pVRCompositor

    def VROverlay(self):
        self.checkClear()
        if self.m_pVROverlay is None:
            self.m_pVROverlay = IVROverlay()
        return self.m_pVROverlay

    def VRResources(self):
        self.checkClear()
        if self.m_pVRResources is None:
            self.m_pVRResources = IVRResources()
        return self.m_pVRResources

    def VRRenderModels(self):
        self.checkClear()
        if self.m_pVRRenderModels is None:
            self.m_pVRRenderModels = IVRRenderModels()
        return self.m_pVRRenderModels

    def VRExtendedDisplay(self):
        self.checkClear()
        if self.m_pVRExtendedDisplay is None:
            self.m_pVRExtendedDisplay = IVRExtendedDisplay()
        return self.m_pVRExtendedDisplay

    def VRSettings(self):
        self.checkClear()
        if self.m_pVRSettings is None:
            self.m_pVRSettings = IVRSettings()
        return self.m_pVRSettings

    def VRApplications(self):
        self.checkClear()
        if self.m_pVRApplications is None:
            self.m_pVRApplications = IVRApplications()
        return self.m_pVRApplications

    def VRTrackedCamera(self):
        self.checkClear()
        if self.m_pVRTrackedCamera is None:
            self.m_pVRTrackedCamera = IVRTrackedCamera()
        return self.m_pVRTrackedCamera

    def VRScreenshots(self):
        self.checkClear()
        if self.m_pVRScreenshots is None:
            self.m_pVRScreenshots = IVRScreenshots()
        return self.m_pVRScreenshots


# Globals for context management
_vr_token = None
_internal_module_context = COpenVRContext()


def VRSystem():
    return _internal_module_context.VRSystem()

def VRChaperone():
    return _internal_module_context.VRChaperone()

def VRChaperoneSetup():
    return _internal_module_context.VRChaperoneSetup()

def VRCompositor():
    return _internal_module_context.VRCompositor()

def VROverlay():
    return _internal_module_context.VROverlay()

def VRResources():
    return _internal_module_context.VRResources()

def VRRenderModels():
    return _internal_module_context.VRRenderModels()

def VRExtendedDisplay():
    return _internal_module_context.VRExtendedDisplay()

def VRSettings():
    return _internal_module_context.VRSettings()

def VRApplications():
    return _internal_module_context.VRApplications()

def VRTrackedCamera():
    return _internal_module_context.VRTrackedCamera()

def VRScreenshots():
    return _internal_module_context.VRScreenshots()

class VREvent_Data_t(Union):
    _fields_ = [
        ("reserved", VREvent_Reserved_t),
        ("controller", VREvent_Controller_t),
        ("mouse", VREvent_Mouse_t),
        ("scroll", VREvent_Scroll_t),
        ("process", VREvent_Process_t),
        ("notification", VREvent_Notification_t),
        ("overlay", VREvent_Overlay_t),
        ("status", VREvent_Status_t),
        ("keyboard", VREvent_Keyboard_t),
        ("ipd", VREvent_Ipd_t),
        ("chaperone", VREvent_Chaperone_t),
        ("performanceTest", VREvent_PerformanceTest_t),
        ("touchPadMove", VREvent_TouchPadMove_t),
        ("seatedZeroPoseReset", VREvent_SeatedZeroPoseReset_t),
    ]


class VREvent_t(Structure):
    "An event posted by the server to all running applications"

    _fields_ = [
        ("eventType", c_uint32),
        ("trackedDeviceIndex", TrackedDeviceIndex_t),
        ("eventAgeSeconds", c_float),
        ("data", VREvent_Data_t),
    ]


class VROverlayIntersectionMaskPrimitive_Data_t(Union):
    _fields_ = [
        ("m_Rectangle", IntersectionMaskRectangle_t),
        ("m_Circle", IntersectionMaskCircle_t),
    ]


class VROverlayIntersectionMaskPrimitive_t(Structure):
    _fields_ = [
        ("m_nPrimitiveType", EVROverlayIntersectionMaskPrimitiveType),
        ("m_Primitive", VROverlayIntersectionMaskPrimitive_Data_t),
    ]


class IVRSystem_FnTable(Structure):
    _fields_ = [
        ("getRecommendedRenderTargetSize", OPENVR_FNTABLE_CALLTYPE(None, POINTER(c_uint32), POINTER(c_uint32))),
        ("getProjectionMatrix", OPENVR_FNTABLE_CALLTYPE(HmdMatrix44_t, EVREye, c_float, c_float)),
        ("getProjectionRaw", OPENVR_FNTABLE_CALLTYPE(None, EVREye, POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float))),
        ("computeDistortion", OPENVR_FNTABLE_CALLTYPE(openvr_bool, EVREye, c_float, c_float, POINTER(DistortionCoordinates_t))),
        ("getEyeToHeadTransform", OPENVR_FNTABLE_CALLTYPE(HmdMatrix34_t, EVREye)),
        ("getTimeSinceLastVsync", OPENVR_FNTABLE_CALLTYPE(openvr_bool, POINTER(c_float), POINTER(c_uint64))),
        ("getD3D9AdapterIndex", OPENVR_FNTABLE_CALLTYPE(c_int32)),
        ("getDXGIOutputInfo", OPENVR_FNTABLE_CALLTYPE(None, POINTER(c_int32))),
        ("isDisplayOnDesktop", OPENVR_FNTABLE_CALLTYPE(openvr_bool)),
        ("setDisplayVisibility", OPENVR_FNTABLE_CALLTYPE(openvr_bool, openvr_bool)),
        ("getDeviceToAbsoluteTrackingPose", OPENVR_FNTABLE_CALLTYPE(None, ETrackingUniverseOrigin, c_float, POINTER(TrackedDevicePose_t), c_uint32)),
        ("resetSeatedZeroPose", OPENVR_FNTABLE_CALLTYPE(None)),
        ("getSeatedZeroPoseToStandingAbsoluteTrackingPose", OPENVR_FNTABLE_CALLTYPE(HmdMatrix34_t)),
        ("getRawZeroPoseToStandingAbsoluteTrackingPose", OPENVR_FNTABLE_CALLTYPE(HmdMatrix34_t)),
        ("getSortedTrackedDeviceIndicesOfClass", OPENVR_FNTABLE_CALLTYPE(c_uint32, ETrackedDeviceClass, POINTER(TrackedDeviceIndex_t), c_uint32, TrackedDeviceIndex_t)),
        ("getTrackedDeviceActivityLevel", OPENVR_FNTABLE_CALLTYPE(EDeviceActivityLevel, TrackedDeviceIndex_t)),
        ("applyTransform", OPENVR_FNTABLE_CALLTYPE(None, POINTER(TrackedDevicePose_t), POINTER(TrackedDevicePose_t), POINTER(HmdMatrix34_t))),
        ("getTrackedDeviceIndexForControllerRole", OPENVR_FNTABLE_CALLTYPE(TrackedDeviceIndex_t, ETrackedControllerRole)),
        ("getControllerRoleForTrackedDeviceIndex", OPENVR_FNTABLE_CALLTYPE(ETrackedControllerRole, TrackedDeviceIndex_t)),
        ("getTrackedDeviceClass", OPENVR_FNTABLE_CALLTYPE(ETrackedDeviceClass, TrackedDeviceIndex_t)),
        ("isTrackedDeviceConnected", OPENVR_FNTABLE_CALLTYPE(openvr_bool, TrackedDeviceIndex_t)),
        ("getBoolTrackedDeviceProperty", OPENVR_FNTABLE_CALLTYPE(openvr_bool, TrackedDeviceIndex_t, ETrackedDeviceProperty, POINTER(ETrackedPropertyError))),
        ("getFloatTrackedDeviceProperty", OPENVR_FNTABLE_CALLTYPE(c_float, TrackedDeviceIndex_t, ETrackedDeviceProperty, POINTER(ETrackedPropertyError))),
        ("getInt32TrackedDeviceProperty", OPENVR_FNTABLE_CALLTYPE(c_int32, TrackedDeviceIndex_t, ETrackedDeviceProperty, POINTER(ETrackedPropertyError))),
        ("getUint64TrackedDeviceProperty", OPENVR_FNTABLE_CALLTYPE(c_uint64, TrackedDeviceIndex_t, ETrackedDeviceProperty, POINTER(ETrackedPropertyError))),
        ("getMatrix34TrackedDeviceProperty", OPENVR_FNTABLE_CALLTYPE(HmdMatrix34_t, TrackedDeviceIndex_t, ETrackedDeviceProperty, POINTER(ETrackedPropertyError))),
        ("getStringTrackedDeviceProperty", OPENVR_FNTABLE_CALLTYPE(c_uint32, TrackedDeviceIndex_t, ETrackedDeviceProperty, c_char_p, c_uint32, POINTER(ETrackedPropertyError))),
        ("getPropErrorNameFromEnum", OPENVR_FNTABLE_CALLTYPE(c_char_p, ETrackedPropertyError)),
        ("pollNextEvent", OPENVR_FNTABLE_CALLTYPE(openvr_bool, POINTER(VREvent_t), c_uint32)),
        ("pollNextEventWithPose", OPENVR_FNTABLE_CALLTYPE(openvr_bool, ETrackingUniverseOrigin, POINTER(VREvent_t), c_uint32, POINTER(TrackedDevicePose_t))),
        ("getEventTypeNameFromEnum", OPENVR_FNTABLE_CALLTYPE(c_char_p, EVREventType)),
        ("getHiddenAreaMesh", OPENVR_FNTABLE_CALLTYPE(HiddenAreaMesh_t, EVREye, EHiddenAreaMeshType)),
        ("getControllerState", OPENVR_FNTABLE_CALLTYPE(openvr_bool, TrackedDeviceIndex_t, POINTER(VRControllerState_t), c_uint32)),
        ("getControllerStateWithPose", OPENVR_FNTABLE_CALLTYPE(openvr_bool, ETrackingUniverseOrigin, TrackedDeviceIndex_t, POINTER(VRControllerState_t), c_uint32, POINTER(TrackedDevicePose_t))),
        ("triggerHapticPulse", OPENVR_FNTABLE_CALLTYPE(None, TrackedDeviceIndex_t, c_uint32, c_ushort)),
        ("getButtonIdNameFromEnum", OPENVR_FNTABLE_CALLTYPE(c_char_p, EVRButtonId)),
        ("getControllerAxisTypeNameFromEnum", OPENVR_FNTABLE_CALLTYPE(c_char_p, EVRControllerAxisType)),
        ("captureInputFocus", OPENVR_FNTABLE_CALLTYPE(openvr_bool)),
        ("releaseInputFocus", OPENVR_FNTABLE_CALLTYPE(None)),
        ("isInputFocusCapturedByAnotherProcess", OPENVR_FNTABLE_CALLTYPE(openvr_bool)),
        ("driverDebugRequest", OPENVR_FNTABLE_CALLTYPE(c_uint32, TrackedDeviceIndex_t, c_char_p, c_char_p, c_uint32)),
        ("performFirmwareUpdate", OPENVR_FNTABLE_CALLTYPE(EVRFirmwareError, TrackedDeviceIndex_t)),
        ("acknowledgeQuit_Exiting", OPENVR_FNTABLE_CALLTYPE(None)),
        ("acknowledgeQuit_UserPrompt", OPENVR_FNTABLE_CALLTYPE(None)),
    ]


class IVRSystem(object):
    def __init__(self):
        version_key = IVRSystem_Version
        if not isInterfaceVersionValid(version_key):
            _checkInitError(VRInitError_Init_InterfaceNotFound)
        # Thank you lukexi https://github.com/lukexi/openvr-hs/blob/master/cbits/openvr_capi_helper.c#L9
        fn_key = b"FnTable:" + version_key
        fn_type = IVRSystem_FnTable
        fn_table_ptr = cast(getGenericInterface(fn_key), POINTER(fn_type))
        if fn_table_ptr is None:
            raise OpenVRError("Error retrieving VR API for IVRSystem")
        self.function_table = fn_table_ptr.contents

    def getRecommendedRenderTargetSize(self):
        "Suggested size for the intermediate render target that the distortion pulls from."

        fn = self.function_table.getRecommendedRenderTargetSize
        pnWidth = c_uint32()
        pnHeight = c_uint32()
        fn(byref(pnWidth), byref(pnHeight))
        return pnWidth.value, pnHeight.value

    def getProjectionMatrix(self, eEye, fNearZ, fFarZ):
        "The projection matrix for the specified eye"

        fn = self.function_table.getProjectionMatrix
        result = fn(eEye, fNearZ, fFarZ)
        return result

    def getProjectionRaw(self, eEye):
        """
        The components necessary to build your own projection matrix in case your
        application is doing something fancy like infinite Z
        """

        fn = self.function_table.getProjectionRaw
        pfLeft = c_float()
        pfRight = c_float()
        pfTop = c_float()
        pfBottom = c_float()
        fn(eEye, byref(pfLeft), byref(pfRight), byref(pfTop), byref(pfBottom))
        return pfLeft.value, pfRight.value, pfTop.value, pfBottom.value

    def computeDistortion(self, eEye, fU, fV):
        """
        Gets the result of the distortion function for the specified eye and input UVs. UVs go from 0,0 in 
        the upper left of that eye's viewport and 1,1 in the lower right of that eye's viewport.
        Returns true for success. Otherwise, returns false, and distortion coordinates are not suitable.
        """

        fn = self.function_table.computeDistortion
        pDistortionCoordinates = DistortionCoordinates_t()
        result = fn(eEye, fU, fV, byref(pDistortionCoordinates))
        return result, pDistortionCoordinates

    def getEyeToHeadTransform(self, eEye):
        """
        Returns the transform from eye space to the head space. Eye space is the per-eye flavor of head
        space that provides stereo disparity. Instead of Model * View * Projection the sequence is Model * View * Eye^-1 * Projection. 
        Normally View and Eye^-1 will be multiplied together and treated as View in your application.
        """

        fn = self.function_table.getEyeToHeadTransform
        result = fn(eEye)
        return result

    def getTimeSinceLastVsync(self):
        """
        Returns the number of elapsed seconds since the last recorded vsync event. This 
        will come from a vsync timer event in the timer if possible or from the application-reported
          time if that is not available. If no vsync times are available the function will 
          return zero for vsync time and frame counter and return false from the method.
        """

        fn = self.function_table.getTimeSinceLastVsync
        pfSecondsSinceLastVsync = c_float()
        pulFrameCounter = c_uint64()
        result = fn(byref(pfSecondsSinceLastVsync), byref(pulFrameCounter))
        return result, pfSecondsSinceLastVsync.value, pulFrameCounter.value

    def getD3D9AdapterIndex(self):
        """
        [D3D9 Only]
        Returns the adapter index that the user should pass into CreateDevice to set up D3D9 in such
        a way that it can go full screen exclusive on the HMD. Returns -1 if there was an error.
        """

        fn = self.function_table.getD3D9AdapterIndex
        result = fn()
        return result

    def getDXGIOutputInfo(self):
        """
        [D3D10/11 Only]
        Returns the adapter index and output index that the user should pass into EnumAdapters and EnumOutputs
        to create the device and swap chain in DX10 and DX11. If an error occurs both indices will be set to -1.
        """

        fn = self.function_table.getDXGIOutputInfo
        pnAdapterIndex = c_int32()
        fn(byref(pnAdapterIndex))
        return pnAdapterIndex.value

    def isDisplayOnDesktop(self):
        "Use to determine if the headset display is part of the desktop (i.e. extended) or hidden (i.e. direct mode)."

        fn = self.function_table.isDisplayOnDesktop
        result = fn()
        return result

    def setDisplayVisibility(self, bIsVisibleOnDesktop):
        "Set the display visibility (true = extended, false = direct mode).  Return value of true indicates that the change was successful."

        fn = self.function_table.setDisplayVisibility
        result = fn(bIsVisibleOnDesktop)
        return result

    def getDeviceToAbsoluteTrackingPose(self, eOrigin, fPredictedSecondsToPhotonsFromNow, unTrackedDevicePoseArrayCount, pTrackedDevicePoseArray=None):
        """
        The pose that the tracker thinks that the HMD will be in at the specified number of seconds into the 
        future. Pass 0 to get the state at the instant the method is called. Most of the time the application should
        calculate the time until the photons will be emitted from the display and pass that time into the method.
        * This is roughly analogous to the inverse of the view matrix in most applications, though 
        many games will need to do some additional rotation or translation on top of the rotation
        and translation provided by the head pose.
        * For devices where bPoseIsValid is true the application can use the pose to position the device
        in question. The provided array can be any size up to k_unMaxTrackedDeviceCount. 
        * Seated experiences should call this method with TrackingUniverseSeated and receive poses relative
        to the seated zero pose. Standing experiences should call this method with TrackingUniverseStanding 
        and receive poses relative to the Chaperone Play Area. TrackingUniverseRawAndUncalibrated should 
        probably not be used unless the application is the Chaperone calibration tool itself, but will provide
        poses relative to the hardware-specific coordinate system in the driver.
        """

        fn = self.function_table.getDeviceToAbsoluteTrackingPose
        if pTrackedDevicePoseArray is None:
            pTrackedDevicePoseArray = (TrackedDevicePose_t * unTrackedDevicePoseArrayCount)()
        pTrackedDevicePoseArray = cast(pTrackedDevicePoseArray, POINTER(TrackedDevicePose_t))
        fn(eOrigin, fPredictedSecondsToPhotonsFromNow, pTrackedDevicePoseArray, unTrackedDevicePoseArrayCount)
        return pTrackedDevicePoseArray

    def resetSeatedZeroPose(self):
        """
        Sets the zero pose for the seated tracker coordinate system to the current position and yaw of the HMD. After 
        ResetSeatedZeroPose all GetDeviceToAbsoluteTrackingPose calls that pass TrackingUniverseSeated as the origin 
        will be relative to this new zero pose. The new zero coordinate system will not change the fact that the Y axis 
        is up in the real world, so the next pose returned from GetDeviceToAbsoluteTrackingPose after a call to 
        ResetSeatedZeroPose may not be exactly an identity matrix.
        * NOTE: This function overrides the user's previously saved seated zero pose and should only be called as the result of a user action. 
        Users are also able to set their seated zero pose via the OpenVR Dashboard.
        """

        fn = self.function_table.resetSeatedZeroPose
        fn()

    def getSeatedZeroPoseToStandingAbsoluteTrackingPose(self):
        """
        Returns the transform from the seated zero pose to the standing absolute tracking system. This allows 
        applications to represent the seated origin to used or transform object positions from one coordinate
        system to the other. 
        * The seated origin may or may not be inside the Play Area or Collision Bounds returned by IVRChaperone. Its position 
        depends on what the user has set from the Dashboard settings and previous calls to ResetSeatedZeroPose.
        """

        fn = self.function_table.getSeatedZeroPoseToStandingAbsoluteTrackingPose
        result = fn()
        return result

    def getRawZeroPoseToStandingAbsoluteTrackingPose(self):
        """
        Returns the transform from the tracking origin to the standing absolute tracking system. This allows
        applications to convert from raw tracking space to the calibrated standing coordinate system.
        """

        fn = self.function_table.getRawZeroPoseToStandingAbsoluteTrackingPose
        result = fn()
        return result

    def getSortedTrackedDeviceIndicesOfClass(self, eTrackedDeviceClass, unTrackedDeviceIndexArrayCount, unRelativeToTrackedDeviceIndex):
        """
        Get a sorted array of device indices of a given class of tracked devices (e.g. controllers).  Devices are sorted right to left
        relative to the specified tracked device (default: hmd -- pass in -1 for absolute tracking space).  Returns the number of devices
        in the list, or the size of the array needed if not large enough.
        """

        fn = self.function_table.getSortedTrackedDeviceIndicesOfClass
        punTrackedDeviceIndexArray = TrackedDeviceIndex_t()
        result = fn(eTrackedDeviceClass, byref(punTrackedDeviceIndexArray), unTrackedDeviceIndexArrayCount, unRelativeToTrackedDeviceIndex)
        return result, punTrackedDeviceIndexArray

    def getTrackedDeviceActivityLevel(self, unDeviceId):
        "Returns the level of activity on the device."

        fn = self.function_table.getTrackedDeviceActivityLevel
        result = fn(unDeviceId)
        return result

    def applyTransform(self):
        """
        Convenience utility to apply the specified transform to the specified pose.
          This properly transforms all pose components, including velocity and angular velocity
        """

        fn = self.function_table.applyTransform
        pOutputPose = TrackedDevicePose_t()
        pTrackedDevicePose = TrackedDevicePose_t()
        pTransform = HmdMatrix34_t()
        fn(byref(pOutputPose), byref(pTrackedDevicePose), byref(pTransform))
        return pOutputPose, pTrackedDevicePose, pTransform

    def getTrackedDeviceIndexForControllerRole(self, unDeviceType):
        "Returns the device index associated with a specific role, for example the left hand or the right hand."

        fn = self.function_table.getTrackedDeviceIndexForControllerRole
        result = fn(unDeviceType)
        return result

    def getControllerRoleForTrackedDeviceIndex(self, unDeviceIndex):
        "Returns the controller type associated with a device index."

        fn = self.function_table.getControllerRoleForTrackedDeviceIndex
        result = fn(unDeviceIndex)
        return result

    def getTrackedDeviceClass(self, unDeviceIndex):
        """
        Returns the device class of a tracked device. If there has not been a device connected in this slot
        since the application started this function will return TrackedDevice_Invalid. For previous detected
        devices the function will return the previously observed device class. 
        * To determine which devices exist on the system, just loop from 0 to k_unMaxTrackedDeviceCount and check
        the device class. Every device with something other than TrackedDevice_Invalid is associated with an 
        actual tracked device.
        """

        fn = self.function_table.getTrackedDeviceClass
        result = fn(unDeviceIndex)
        return result

    def isTrackedDeviceConnected(self, unDeviceIndex):
        "Returns true if there is a device connected in this slot."

        fn = self.function_table.isTrackedDeviceConnected
        result = fn(unDeviceIndex)
        return result

    def getBoolTrackedDeviceProperty(self, unDeviceIndex, prop):
        "Returns a bool property. If the device index is not valid or the property is not a bool type this function will return false."

        fn = self.function_table.getBoolTrackedDeviceProperty
        pError = ETrackedPropertyError()
        result = fn(unDeviceIndex, prop, byref(pError))
        return result, pError

    def getFloatTrackedDeviceProperty(self, unDeviceIndex, prop):
        "Returns a float property. If the device index is not valid or the property is not a float type this function will return 0."

        fn = self.function_table.getFloatTrackedDeviceProperty
        pError = ETrackedPropertyError()
        result = fn(unDeviceIndex, prop, byref(pError))
        return result, pError

    def getInt32TrackedDeviceProperty(self, unDeviceIndex, prop):
        "Returns an int property. If the device index is not valid or the property is not a int type this function will return 0."

        fn = self.function_table.getInt32TrackedDeviceProperty
        pError = ETrackedPropertyError()
        result = fn(unDeviceIndex, prop, byref(pError))
        return result, pError

    def getUint64TrackedDeviceProperty(self, unDeviceIndex, prop):
        "Returns a uint64 property. If the device index is not valid or the property is not a uint64 type this function will return 0."

        fn = self.function_table.getUint64TrackedDeviceProperty
        pError = ETrackedPropertyError()
        result = fn(unDeviceIndex, prop, byref(pError))
        return result, pError

    def getMatrix34TrackedDeviceProperty(self, unDeviceIndex, prop):
        "Returns a matrix property. If the device index is not valid or the property is not a matrix type, this function will return identity."

        fn = self.function_table.getMatrix34TrackedDeviceProperty
        pError = ETrackedPropertyError()
        result = fn(unDeviceIndex, prop, byref(pError))
        return result, pError

    def getStringTrackedDeviceProperty(self, unDeviceIndex, prop):
        """
        Returns a string property. If the device index is not valid or the property is not a string type this function will 
        return 0. Otherwise it returns the length of the number of bytes necessary to hold this string including the trailing
        null. Strings will always fit in buffers of k_unMaxPropertyStringSize characters.
        """

        fn = self.function_table.getStringTrackedDeviceProperty
        pError = ETrackedPropertyError()
        # TODO: automate this string argument manipulation ****
        unRequiredBufferLen = fn( unDeviceIndex, prop, None, 0, byref(pError) )
        if unRequiredBufferLen == 0:
            return b""
        pchBuffer = ctypes.create_string_buffer(unRequiredBufferLen)
        fn( unDeviceIndex, prop, pchBuffer, unRequiredBufferLen, byref(pError) )
        if pError.value != TrackedProp_Success:
            raise OpenVRError(str(pError))
        sResult = bytes(pchBuffer.value)
        return sResult

    def getPropErrorNameFromEnum(self, error):
        """
        returns a string that corresponds with the specified property error. The string will be the name 
        of the error enum value for all valid error codes
        """

        fn = self.function_table.getPropErrorNameFromEnum
        result = fn(error)
        return result

    def pollNextEvent(self, pEvent):
        """
        Returns true and fills the event with the next event on the queue if there is one. If there are no events
        this method returns false. uncbVREvent should be the size in bytes of the VREvent_t struct
        """

        fn = self.function_table.pollNextEvent
        # TODO: Automate this manually converted method
        result = fn(byref(pEvent), sizeof(VREvent_t))
        return result != 0

    def pollNextEventWithPose(self, eOrigin, uncbVREvent):
        """
        Returns true and fills the event with the next event on the queue if there is one. If there are no events
        this method returns false. Fills in the pose of the associated tracked device in the provided pose struct. 
        This pose will always be older than the call to this function and should not be used to render the device. 
        uncbVREvent should be the size in bytes of the VREvent_t struct
        """

        fn = self.function_table.pollNextEventWithPose
        pEvent = VREvent_t()
        pTrackedDevicePose = TrackedDevicePose_t()
        result = fn(eOrigin, byref(pEvent), uncbVREvent, byref(pTrackedDevicePose))
        return result, pEvent, pTrackedDevicePose

    def getEventTypeNameFromEnum(self, eType):
        "returns the name of an EVREvent enum value"

        fn = self.function_table.getEventTypeNameFromEnum
        result = fn(eType)
        return result

    def getHiddenAreaMesh(self, eEye, type_):
        """
        Returns the hidden area mesh for the current HMD. The pixels covered by this mesh will never be seen by the user after the lens distortion is
        applied based on visibility to the panels. If this HMD does not have a hidden area mesh, the vertex data and count will be NULL and 0 respectively.
        This mesh is meant to be rendered into the stencil buffer (or into the depth buffer setting nearz) before rendering each eye's view. 
        This will improve performance by letting the GPU early-reject pixels the user will never see before running the pixel shader.
        NOTE: Render this mesh with backface culling disabled since the winding order of the vertices can be different per-HMD or per-eye.
        Setting the bInverse argument to true will produce the visible area mesh that is commonly used in place of full-screen quads. The visible area mesh covers all of the pixels the hidden area mesh does not cover.
        Setting the bLineLoop argument will return a line loop of vertices in HiddenAreaMesh_t->pVertexData with HiddenAreaMesh_t->unTriangleCount set to the number of vertices.
        """

        fn = self.function_table.getHiddenAreaMesh
        result = fn(eEye, type_)
        return result

    def getControllerState(self, unControllerDeviceIndex, unControllerStateSize=sizeof(VRControllerState_t)):
        """
        Fills the supplied struct with the current state of the controller. Returns false if the controller index
        is invalid.
        """

        fn = self.function_table.getControllerState
        pControllerState = VRControllerState_t()
        result = fn(unControllerDeviceIndex, byref(pControllerState), unControllerStateSize)
        return result, pControllerState

    def getControllerStateWithPose(self, eOrigin, unControllerDeviceIndex, unControllerStateSize=sizeof(VRControllerState_t)):
        """
        fills the supplied struct with the current state of the controller and the provided pose with the pose of 
        the controller when the controller state was updated most recently. Use this form if you need a precise controller
        pose as input to your application when the user presses or releases a button.
        """

        fn = self.function_table.getControllerStateWithPose
        pControllerState = VRControllerState_t()
        pTrackedDevicePose = TrackedDevicePose_t()
        result = fn(eOrigin, unControllerDeviceIndex, byref(pControllerState), unControllerStateSize, byref(pTrackedDevicePose))
        return result, pControllerState, pTrackedDevicePose

    def triggerHapticPulse(self, unControllerDeviceIndex, unAxisId, usDurationMicroSec):
        """
        Trigger a single haptic pulse on a controller. After this call the application may not trigger another haptic pulse on this controller
        and axis combination for 5ms.
        """

        fn = self.function_table.triggerHapticPulse
        fn(unControllerDeviceIndex, unAxisId, usDurationMicroSec)

    def getButtonIdNameFromEnum(self, eButtonId):
        "returns the name of an EVRButtonId enum value"

        fn = self.function_table.getButtonIdNameFromEnum
        result = fn(eButtonId)
        return result

    def getControllerAxisTypeNameFromEnum(self, eAxisType):
        "returns the name of an EVRControllerAxisType enum value"

        fn = self.function_table.getControllerAxisTypeNameFromEnum
        result = fn(eAxisType)
        return result

    def captureInputFocus(self):
        """
        Tells OpenVR that this process wants exclusive access to controller button states and button events. Other apps will be notified that 
        they have lost input focus with a VREvent_InputFocusCaptured event. Returns false if input focus could not be captured for
        some reason.
        """

        fn = self.function_table.captureInputFocus
        result = fn()
        return result

    def releaseInputFocus(self):
        """
        Tells OpenVR that this process no longer wants exclusive access to button states and button events. Other apps will be notified 
        that input focus has been released with a VREvent_InputFocusReleased event.
        """

        fn = self.function_table.releaseInputFocus
        fn()

    def isInputFocusCapturedByAnotherProcess(self):
        "Returns true if input focus is captured by another process."

        fn = self.function_table.isInputFocusCapturedByAnotherProcess
        result = fn()
        return result

    def driverDebugRequest(self, unDeviceIndex, pchRequest, pchResponseBuffer, unResponseBufferSize):
        """
        Sends a request to the driver for the specified device and returns the response. The maximum response size is 32k,
        but this method can be called with a smaller buffer. If the response exceeds the size of the buffer, it is truncated. 
        The size of the response including its terminating null is returned.
        """

        fn = self.function_table.driverDebugRequest
        result = fn(unDeviceIndex, pchRequest, pchResponseBuffer, unResponseBufferSize)
        return result

    def performFirmwareUpdate(self, unDeviceIndex):
        """
        Performs the actual firmware update if applicable. 
        The following events will be sent, if VRFirmwareError_None was returned: VREvent_FirmwareUpdateStarted, VREvent_FirmwareUpdateFinished 
        Use the properties Prop_Firmware_UpdateAvailable_Bool, Prop_Firmware_ManualUpdate_Bool, and Prop_Firmware_ManualUpdateURL_String
        to figure our whether a firmware update is available, and to figure out whether its a manual update 
        Prop_Firmware_ManualUpdateURL_String should point to an URL describing the manual update process
        """

        fn = self.function_table.performFirmwareUpdate
        result = fn(unDeviceIndex)
        return result

    def acknowledgeQuit_Exiting(self):
        """
        Call this to acknowledge to the system that VREvent_Quit has been received and that the process is exiting.
        This extends the timeout until the process is killed.
        """

        fn = self.function_table.acknowledgeQuit_Exiting
        fn()

    def acknowledgeQuit_UserPrompt(self):
        """
        Call this to tell the system that the user is being prompted to save data. This
        halts the timeout and dismisses the dashboard (if it was up). Applications should be sure to actually 
        prompt the user to save and then exit afterward, otherwise the user will be left in a confusing state.
        """

        fn = self.function_table.acknowledgeQuit_UserPrompt
        fn()



class IVRExtendedDisplay_FnTable(Structure):
    _fields_ = [
        ("getWindowBounds", OPENVR_FNTABLE_CALLTYPE(None, POINTER(c_int32), POINTER(c_int32), POINTER(c_uint32), POINTER(c_uint32))),
        ("getEyeOutputViewport", OPENVR_FNTABLE_CALLTYPE(None, EVREye, POINTER(c_uint32), POINTER(c_uint32), POINTER(c_uint32), POINTER(c_uint32))),
        ("getDXGIOutputInfo", OPENVR_FNTABLE_CALLTYPE(None, POINTER(c_int32), POINTER(c_int32))),
    ]


class IVRExtendedDisplay(object):
    """
    NOTE: Use of this interface is not recommended in production applications. It will not work for displays which use
    direct-to-display mode. Creating our own window is also incompatible with the VR compositor and is not available when the compositor is running.
    """

    def __init__(self):
        version_key = IVRExtendedDisplay_Version
        if not isInterfaceVersionValid(version_key):
            _checkInitError(VRInitError_Init_InterfaceNotFound)
        # Thank you lukexi https://github.com/lukexi/openvr-hs/blob/master/cbits/openvr_capi_helper.c#L9
        fn_key = b"FnTable:" + version_key
        fn_type = IVRExtendedDisplay_FnTable
        fn_table_ptr = cast(getGenericInterface(fn_key), POINTER(fn_type))
        if fn_table_ptr is None:
            raise OpenVRError("Error retrieving VR API for IVRExtendedDisplay")
        self.function_table = fn_table_ptr.contents

    def getWindowBounds(self):
        "Size and position that the window needs to be on the VR display."

        fn = self.function_table.getWindowBounds
        pnX = c_int32()
        pnY = c_int32()
        pnWidth = c_uint32()
        pnHeight = c_uint32()
        fn(byref(pnX), byref(pnY), byref(pnWidth), byref(pnHeight))
        return pnX.value, pnY.value, pnWidth.value, pnHeight.value

    def getEyeOutputViewport(self, eEye):
        "Gets the viewport in the frame buffer to draw the output of the distortion into"

        fn = self.function_table.getEyeOutputViewport
        pnX = c_uint32()
        pnY = c_uint32()
        pnWidth = c_uint32()
        pnHeight = c_uint32()
        fn(eEye, byref(pnX), byref(pnY), byref(pnWidth), byref(pnHeight))
        return pnX.value, pnY.value, pnWidth.value, pnHeight.value

    def getDXGIOutputInfo(self):
        """
        [D3D10/11 Only]
        Returns the adapter index and output index that the user should pass into EnumAdapters and EnumOutputs
        to create the device and swap chain in DX10 and DX11. If an error occurs both indices will be set to -1.
        """

        fn = self.function_table.getDXGIOutputInfo
        pnAdapterIndex = c_int32()
        pnAdapterOutputIndex = c_int32()
        fn(byref(pnAdapterIndex), byref(pnAdapterOutputIndex))
        return pnAdapterIndex.value, pnAdapterOutputIndex.value



class IVRTrackedCamera_FnTable(Structure):
    _fields_ = [
        ("getCameraErrorNameFromEnum", OPENVR_FNTABLE_CALLTYPE(c_char_p, EVRTrackedCameraError)),
        ("hasCamera", OPENVR_FNTABLE_CALLTYPE(EVRTrackedCameraError, TrackedDeviceIndex_t, POINTER(openvr_bool))),
        ("getCameraFrameSize", OPENVR_FNTABLE_CALLTYPE(EVRTrackedCameraError, TrackedDeviceIndex_t, EVRTrackedCameraFrameType, POINTER(c_uint32), POINTER(c_uint32), POINTER(c_uint32))),
        ("getCameraIntrinsics", OPENVR_FNTABLE_CALLTYPE(EVRTrackedCameraError, TrackedDeviceIndex_t, EVRTrackedCameraFrameType, POINTER(HmdVector2_t), POINTER(HmdVector2_t))),
        ("getCameraProjection", OPENVR_FNTABLE_CALLTYPE(EVRTrackedCameraError, TrackedDeviceIndex_t, EVRTrackedCameraFrameType, c_float, c_float, POINTER(HmdMatrix44_t))),
        ("acquireVideoStreamingService", OPENVR_FNTABLE_CALLTYPE(EVRTrackedCameraError, TrackedDeviceIndex_t, POINTER(TrackedCameraHandle_t))),
        ("releaseVideoStreamingService", OPENVR_FNTABLE_CALLTYPE(EVRTrackedCameraError, TrackedCameraHandle_t)),
        ("getVideoStreamFrameBuffer", OPENVR_FNTABLE_CALLTYPE(EVRTrackedCameraError, TrackedCameraHandle_t, EVRTrackedCameraFrameType, c_void_p, c_uint32, POINTER(CameraVideoStreamFrameHeader_t), c_uint32)),
        ("getVideoStreamTextureSize", OPENVR_FNTABLE_CALLTYPE(EVRTrackedCameraError, TrackedDeviceIndex_t, EVRTrackedCameraFrameType, POINTER(VRTextureBounds_t), POINTER(c_uint32), POINTER(c_uint32))),
        ("getVideoStreamTextureD3D11", OPENVR_FNTABLE_CALLTYPE(EVRTrackedCameraError, TrackedCameraHandle_t, EVRTrackedCameraFrameType, c_void_p, POINTER(c_void_p), POINTER(CameraVideoStreamFrameHeader_t), c_uint32)),
        ("getVideoStreamTextureGL", OPENVR_FNTABLE_CALLTYPE(EVRTrackedCameraError, TrackedCameraHandle_t, EVRTrackedCameraFrameType, POINTER(glUInt_t), POINTER(CameraVideoStreamFrameHeader_t), c_uint32)),
        ("releaseVideoStreamTextureGL", OPENVR_FNTABLE_CALLTYPE(EVRTrackedCameraError, TrackedCameraHandle_t, glUInt_t)),
    ]


class IVRTrackedCamera(object):
    def __init__(self):
        version_key = IVRTrackedCamera_Version
        if not isInterfaceVersionValid(version_key):
            _checkInitError(VRInitError_Init_InterfaceNotFound)
        # Thank you lukexi https://github.com/lukexi/openvr-hs/blob/master/cbits/openvr_capi_helper.c#L9
        fn_key = b"FnTable:" + version_key
        fn_type = IVRTrackedCamera_FnTable
        fn_table_ptr = cast(getGenericInterface(fn_key), POINTER(fn_type))
        if fn_table_ptr is None:
            raise OpenVRError("Error retrieving VR API for IVRTrackedCamera")
        self.function_table = fn_table_ptr.contents

    def getCameraErrorNameFromEnum(self, eCameraError):
        "Returns a string for an error"

        fn = self.function_table.getCameraErrorNameFromEnum
        result = fn(eCameraError)
        return result

    def hasCamera(self, nDeviceIndex):
        "For convenience, same as tracked property request Prop_HasCamera_Bool"

        fn = self.function_table.hasCamera
        pHasCamera = openvr_bool()
        result = fn(nDeviceIndex, byref(pHasCamera))
        return result, pHasCamera

    def getCameraFrameSize(self, nDeviceIndex, eFrameType):
        "Gets size of the image frame."

        fn = self.function_table.getCameraFrameSize
        pnWidth = c_uint32()
        pnHeight = c_uint32()
        pnFrameBufferSize = c_uint32()
        result = fn(nDeviceIndex, eFrameType, byref(pnWidth), byref(pnHeight), byref(pnFrameBufferSize))
        return result, pnWidth.value, pnHeight.value, pnFrameBufferSize.value

    def getCameraIntrinsics(self, nDeviceIndex, eFrameType):
        fn = self.function_table.getCameraIntrinsics
        pFocalLength = HmdVector2_t()
        pCenter = HmdVector2_t()
        result = fn(nDeviceIndex, eFrameType, byref(pFocalLength), byref(pCenter))
        return result, pFocalLength, pCenter

    def getCameraProjection(self, nDeviceIndex, eFrameType, flZNear, flZFar):
        fn = self.function_table.getCameraProjection
        pProjection = HmdMatrix44_t()
        result = fn(nDeviceIndex, eFrameType, flZNear, flZFar, byref(pProjection))
        return result, pProjection

    def acquireVideoStreamingService(self, nDeviceIndex):
        """
        Acquiring streaming service permits video streaming for the caller. Releasing hints the system that video services do not need to be maintained for this client.
        If the camera has not already been activated, a one time spin up may incur some auto exposure as well as initial streaming frame delays.
        The camera should be considered a global resource accessible for shared consumption but not exclusive to any caller.
        The camera may go inactive due to lack of active consumers or headset idleness.
        """

        fn = self.function_table.acquireVideoStreamingService
        pHandle = TrackedCameraHandle_t()
        result = fn(nDeviceIndex, byref(pHandle))
        return result, pHandle

    def releaseVideoStreamingService(self, hTrackedCamera):
        fn = self.function_table.releaseVideoStreamingService
        result = fn(hTrackedCamera)
        return result

    def getVideoStreamFrameBuffer(self, hTrackedCamera, eFrameType, pFrameBuffer, nFrameBufferSize, nFrameHeaderSize):
        """
        Copies the image frame into a caller's provided buffer. The image data is currently provided as RGBA data, 4 bytes per pixel.
        A caller can provide null for the framebuffer or frameheader if not desired. Requesting the frame header first, followed by the frame buffer allows
        the caller to determine if the frame as advanced per the frame header sequence. 
        If there is no frame available yet, due to initial camera spinup or re-activation, the error will be VRTrackedCameraError_NoFrameAvailable.
        Ideally a caller should be polling at ~16ms intervals
        """

        fn = self.function_table.getVideoStreamFrameBuffer
        pFrameHeader = CameraVideoStreamFrameHeader_t()
        result = fn(hTrackedCamera, eFrameType, pFrameBuffer, nFrameBufferSize, byref(pFrameHeader), nFrameHeaderSize)
        return result, pFrameHeader

    def getVideoStreamTextureSize(self, nDeviceIndex, eFrameType):
        "Gets size of the image frame."

        fn = self.function_table.getVideoStreamTextureSize
        pTextureBounds = VRTextureBounds_t()
        pnWidth = c_uint32()
        pnHeight = c_uint32()
        result = fn(nDeviceIndex, eFrameType, byref(pTextureBounds), byref(pnWidth), byref(pnHeight))
        return result, pTextureBounds, pnWidth.value, pnHeight.value

    def getVideoStreamTextureD3D11(self, hTrackedCamera, eFrameType, pD3D11DeviceOrResource, nFrameHeaderSize):
        """
        Access a shared D3D11 texture for the specified tracked camera stream.
        The camera frame type VRTrackedCameraFrameType_Undistorted is not supported directly as a shared texture. It is an interior subregion of the shared texture VRTrackedCameraFrameType_MaximumUndistorted.
        Instead, use GetVideoStreamTextureSize() with VRTrackedCameraFrameType_Undistorted to determine the proper interior subregion bounds along with GetVideoStreamTextureD3D11() with
        VRTrackedCameraFrameType_MaximumUndistorted to provide the texture. The VRTrackedCameraFrameType_MaximumUndistorted will yield an image where the invalid regions are decoded
        by the alpha channel having a zero component. The valid regions all have a non-zero alpha component. The subregion as described by VRTrackedCameraFrameType_Undistorted 
        guarantees a rectangle where all pixels are valid.
        """

        fn = self.function_table.getVideoStreamTextureD3D11
        ppD3D11ShaderResourceView = c_void_p()
        pFrameHeader = CameraVideoStreamFrameHeader_t()
        result = fn(hTrackedCamera, eFrameType, pD3D11DeviceOrResource, byref(ppD3D11ShaderResourceView), byref(pFrameHeader), nFrameHeaderSize)
        return result, ppD3D11ShaderResourceView.value, pFrameHeader

    def getVideoStreamTextureGL(self, hTrackedCamera, eFrameType, nFrameHeaderSize):
        "Access a shared GL texture for the specified tracked camera stream"

        fn = self.function_table.getVideoStreamTextureGL
        pglTextureId = glUInt_t()
        pFrameHeader = CameraVideoStreamFrameHeader_t()
        result = fn(hTrackedCamera, eFrameType, byref(pglTextureId), byref(pFrameHeader), nFrameHeaderSize)
        return result, pglTextureId, pFrameHeader

    def releaseVideoStreamTextureGL(self, hTrackedCamera, glTextureId):
        fn = self.function_table.releaseVideoStreamTextureGL
        result = fn(hTrackedCamera, glTextureId)
        return result



class IVRApplications_FnTable(Structure):
    _fields_ = [
        ("addApplicationManifest", OPENVR_FNTABLE_CALLTYPE(EVRApplicationError, c_char_p, openvr_bool)),
        ("removeApplicationManifest", OPENVR_FNTABLE_CALLTYPE(EVRApplicationError, c_char_p)),
        ("isApplicationInstalled", OPENVR_FNTABLE_CALLTYPE(openvr_bool, c_char_p)),
        ("getApplicationCount", OPENVR_FNTABLE_CALLTYPE(c_uint32)),
        ("getApplicationKeyByIndex", OPENVR_FNTABLE_CALLTYPE(EVRApplicationError, c_uint32, c_char_p, c_uint32)),
        ("getApplicationKeyByProcessId", OPENVR_FNTABLE_CALLTYPE(EVRApplicationError, c_uint32, c_char_p, c_uint32)),
        ("launchApplication", OPENVR_FNTABLE_CALLTYPE(EVRApplicationError, c_char_p)),
        ("launchTemplateApplication", OPENVR_FNTABLE_CALLTYPE(EVRApplicationError, c_char_p, c_char_p, POINTER(AppOverrideKeys_t), c_uint32)),
        ("launchApplicationFromMimeType", OPENVR_FNTABLE_CALLTYPE(EVRApplicationError, c_char_p, c_char_p)),
        ("launchDashboardOverlay", OPENVR_FNTABLE_CALLTYPE(EVRApplicationError, c_char_p)),
        ("cancelApplicationLaunch", OPENVR_FNTABLE_CALLTYPE(openvr_bool, c_char_p)),
        ("identifyApplication", OPENVR_FNTABLE_CALLTYPE(EVRApplicationError, c_uint32, c_char_p)),
        ("getApplicationProcessId", OPENVR_FNTABLE_CALLTYPE(c_uint32, c_char_p)),
        ("getApplicationsErrorNameFromEnum", OPENVR_FNTABLE_CALLTYPE(c_char_p, EVRApplicationError)),
        ("getApplicationPropertyString", OPENVR_FNTABLE_CALLTYPE(c_uint32, c_char_p, EVRApplicationProperty, c_char_p, c_uint32, POINTER(EVRApplicationError))),
        ("getApplicationPropertyBool", OPENVR_FNTABLE_CALLTYPE(openvr_bool, c_char_p, EVRApplicationProperty, POINTER(EVRApplicationError))),
        ("getApplicationPropertyUint64", OPENVR_FNTABLE_CALLTYPE(c_uint64, c_char_p, EVRApplicationProperty, POINTER(EVRApplicationError))),
        ("setApplicationAutoLaunch", OPENVR_FNTABLE_CALLTYPE(EVRApplicationError, c_char_p, openvr_bool)),
        ("getApplicationAutoLaunch", OPENVR_FNTABLE_CALLTYPE(openvr_bool, c_char_p)),
        ("setDefaultApplicationForMimeType", OPENVR_FNTABLE_CALLTYPE(EVRApplicationError, c_char_p, c_char_p)),
        ("getDefaultApplicationForMimeType", OPENVR_FNTABLE_CALLTYPE(openvr_bool, c_char_p, c_char_p, c_uint32)),
        ("getApplicationSupportedMimeTypes", OPENVR_FNTABLE_CALLTYPE(openvr_bool, c_char_p, c_char_p, c_uint32)),
        ("getApplicationsThatSupportMimeType", OPENVR_FNTABLE_CALLTYPE(c_uint32, c_char_p, c_char_p, c_uint32)),
        ("getApplicationLaunchArguments", OPENVR_FNTABLE_CALLTYPE(c_uint32, c_uint32, c_char_p, c_uint32)),
        ("getStartingApplication", OPENVR_FNTABLE_CALLTYPE(EVRApplicationError, c_char_p, c_uint32)),
        ("getTransitionState", OPENVR_FNTABLE_CALLTYPE(EVRApplicationTransitionState)),
        ("performApplicationPrelaunchCheck", OPENVR_FNTABLE_CALLTYPE(EVRApplicationError, c_char_p)),
        ("getApplicationsTransitionStateNameFromEnum", OPENVR_FNTABLE_CALLTYPE(c_char_p, EVRApplicationTransitionState)),
        ("isQuitUserPromptRequested", OPENVR_FNTABLE_CALLTYPE(openvr_bool)),
        ("launchInternalProcess", OPENVR_FNTABLE_CALLTYPE(EVRApplicationError, c_char_p, c_char_p, c_char_p)),
        ("getCurrentSceneProcessId", OPENVR_FNTABLE_CALLTYPE(c_uint32)),
    ]


class IVRApplications(object):
    def __init__(self):
        version_key = IVRApplications_Version
        if not isInterfaceVersionValid(version_key):
            _checkInitError(VRInitError_Init_InterfaceNotFound)
        # Thank you lukexi https://github.com/lukexi/openvr-hs/blob/master/cbits/openvr_capi_helper.c#L9
        fn_key = b"FnTable:" + version_key
        fn_type = IVRApplications_FnTable
        fn_table_ptr = cast(getGenericInterface(fn_key), POINTER(fn_type))
        if fn_table_ptr is None:
            raise OpenVRError("Error retrieving VR API for IVRApplications")
        self.function_table = fn_table_ptr.contents

    def addApplicationManifest(self, pchApplicationManifestFullPath, bTemporary):
        """
        Adds an application manifest to the list to load when building the list of installed applications. 
        Temporary manifests are not automatically loaded
        """

        fn = self.function_table.addApplicationManifest
        result = fn(pchApplicationManifestFullPath, bTemporary)
        return result

    def removeApplicationManifest(self, pchApplicationManifestFullPath):
        "Removes an application manifest from the list to load when building the list of installed applications."

        fn = self.function_table.removeApplicationManifest
        result = fn(pchApplicationManifestFullPath)
        return result

    def isApplicationInstalled(self, pchAppKey):
        "Returns true if an application is installed"

        fn = self.function_table.isApplicationInstalled
        result = fn(pchAppKey)
        return result

    def getApplicationCount(self):
        "Returns the number of applications available in the list"

        fn = self.function_table.getApplicationCount
        result = fn()
        return result

    def getApplicationKeyByIndex(self, unApplicationIndex, pchAppKeyBuffer, unAppKeyBufferLen):
        """
        Returns the key of the specified application. The index is at least 0 and is less than the return 
        value of GetApplicationCount(). The buffer should be at least k_unMaxApplicationKeyLength in order to 
        fit the key.
        """

        fn = self.function_table.getApplicationKeyByIndex
        result = fn(unApplicationIndex, pchAppKeyBuffer, unAppKeyBufferLen)
        return result

    def getApplicationKeyByProcessId(self, unProcessId, pchAppKeyBuffer, unAppKeyBufferLen):
        """
        Returns the key of the application for the specified Process Id. The buffer should be at least 
        k_unMaxApplicationKeyLength in order to fit the key.
        """

        fn = self.function_table.getApplicationKeyByProcessId
        result = fn(unProcessId, pchAppKeyBuffer, unAppKeyBufferLen)
        return result

    def launchApplication(self, pchAppKey):
        """
        Launches the application. The existing scene application will exit and then the new application will start.
        This call is not valid for dashboard overlay applications.
        """

        fn = self.function_table.launchApplication
        result = fn(pchAppKey)
        return result

    def launchTemplateApplication(self, pchTemplateAppKey, pchNewAppKey, unKeys):
        """
        Launches an instance of an application of type template, with its app key being pchNewAppKey (which must be unique) and optionally override sections
        from the manifest file via AppOverrideKeys_t
        """

        fn = self.function_table.launchTemplateApplication
        pKeys = AppOverrideKeys_t()
        result = fn(pchTemplateAppKey, pchNewAppKey, byref(pKeys), unKeys)
        return result, pKeys

    def launchApplicationFromMimeType(self, pchMimeType, pchArgs):
        "launches the application currently associated with this mime type and passes it the option args, typically the filename or object name of the item being launched"

        fn = self.function_table.launchApplicationFromMimeType
        result = fn(pchMimeType, pchArgs)
        return result

    def launchDashboardOverlay(self, pchAppKey):
        """
        Launches the dashboard overlay application if it is not already running. This call is only valid for 
        dashboard overlay applications.
        """

        fn = self.function_table.launchDashboardOverlay
        result = fn(pchAppKey)
        return result

    def cancelApplicationLaunch(self, pchAppKey):
        "Cancel a pending launch for an application"

        fn = self.function_table.cancelApplicationLaunch
        result = fn(pchAppKey)
        return result

    def identifyApplication(self, unProcessId, pchAppKey):
        """
        Identifies a running application. OpenVR can't always tell which process started in response
        to a URL. This function allows a URL handler (or the process itself) to identify the app key 
        for the now running application. Passing a process ID of 0 identifies the calling process. 
        The application must be one that's known to the system via a call to AddApplicationManifest.
        """

        fn = self.function_table.identifyApplication
        result = fn(unProcessId, pchAppKey)
        return result

    def getApplicationProcessId(self, pchAppKey):
        "Returns the process ID for an application. Return 0 if the application was not found or is not running."

        fn = self.function_table.getApplicationProcessId
        result = fn(pchAppKey)
        return result

    def getApplicationsErrorNameFromEnum(self, error):
        "Returns a string for an applications error"

        fn = self.function_table.getApplicationsErrorNameFromEnum
        result = fn(error)
        return result

    def getApplicationPropertyString(self, pchAppKey, eProperty, pchPropertyValueBuffer, unPropertyValueBufferLen):
        "Returns a value for an application property. The required buffer size to fit this value will be returned."

        fn = self.function_table.getApplicationPropertyString
        peError = EVRApplicationError()
        result = fn(pchAppKey, eProperty, pchPropertyValueBuffer, unPropertyValueBufferLen, byref(peError))
        return result, peError

    def getApplicationPropertyBool(self, pchAppKey, eProperty):
        "Returns a bool value for an application property. Returns false in all error cases."

        fn = self.function_table.getApplicationPropertyBool
        peError = EVRApplicationError()
        result = fn(pchAppKey, eProperty, byref(peError))
        return result, peError

    def getApplicationPropertyUint64(self, pchAppKey, eProperty):
        "Returns a uint64 value for an application property. Returns 0 in all error cases."

        fn = self.function_table.getApplicationPropertyUint64
        peError = EVRApplicationError()
        result = fn(pchAppKey, eProperty, byref(peError))
        return result, peError

    def setApplicationAutoLaunch(self, pchAppKey, bAutoLaunch):
        "Sets the application auto-launch flag. This is only valid for applications which return true for VRApplicationProperty_IsDashboardOverlay_Bool."

        fn = self.function_table.setApplicationAutoLaunch
        result = fn(pchAppKey, bAutoLaunch)
        return result

    def getApplicationAutoLaunch(self, pchAppKey):
        "Gets the application auto-launch flag. This is only valid for applications which return true for VRApplicationProperty_IsDashboardOverlay_Bool."

        fn = self.function_table.getApplicationAutoLaunch
        result = fn(pchAppKey)
        return result

    def setDefaultApplicationForMimeType(self, pchAppKey, pchMimeType):
        "Adds this mime-type to the list of supported mime types for this application"

        fn = self.function_table.setDefaultApplicationForMimeType
        result = fn(pchAppKey, pchMimeType)
        return result

    def getDefaultApplicationForMimeType(self, pchMimeType, pchAppKeyBuffer, unAppKeyBufferLen):
        "return the app key that will open this mime type"

        fn = self.function_table.getDefaultApplicationForMimeType
        result = fn(pchMimeType, pchAppKeyBuffer, unAppKeyBufferLen)
        return result

    def getApplicationSupportedMimeTypes(self, pchAppKey, pchMimeTypesBuffer, unMimeTypesBuffer):
        "Get the list of supported mime types for this application, comma-delimited"

        fn = self.function_table.getApplicationSupportedMimeTypes
        result = fn(pchAppKey, pchMimeTypesBuffer, unMimeTypesBuffer)
        return result

    def getApplicationsThatSupportMimeType(self, pchMimeType, pchAppKeysThatSupportBuffer, unAppKeysThatSupportBuffer):
        "Get the list of app-keys that support this mime type, comma-delimited, the return value is number of bytes you need to return the full string"

        fn = self.function_table.getApplicationsThatSupportMimeType
        result = fn(pchMimeType, pchAppKeysThatSupportBuffer, unAppKeysThatSupportBuffer)
        return result

    def getApplicationLaunchArguments(self, unHandle, pchArgs, unArgs):
        "Get the args list from an app launch that had the process already running, you call this when you get a VREvent_ApplicationMimeTypeLoad"

        fn = self.function_table.getApplicationLaunchArguments
        result = fn(unHandle, pchArgs, unArgs)
        return result

    def getStartingApplication(self, pchAppKeyBuffer, unAppKeyBufferLen):
        "Returns the app key for the application that is starting up"

        fn = self.function_table.getStartingApplication
        result = fn(pchAppKeyBuffer, unAppKeyBufferLen)
        return result

    def getTransitionState(self):
        "Returns the application transition state"

        fn = self.function_table.getTransitionState
        result = fn()
        return result

    def performApplicationPrelaunchCheck(self, pchAppKey):
        """
        Returns errors that would prevent the specified application from launching immediately. Calling this function will
        cause the current scene application to quit, so only call it when you are actually about to launch something else.
        What the caller should do about these failures depends on the failure:
          VRApplicationError_OldApplicationQuitting - An existing application has been told to quit. Wait for a VREvent_ProcessQuit
                                                      and try again.
          VRApplicationError_ApplicationAlreadyStarting - This application is already starting. This is a permanent failure.
          VRApplicationError_LaunchInProgress	      - A different application is already starting. This is a permanent failure.
          VRApplicationError_None                   - Go ahead and launch. Everything is clear.
        """

        fn = self.function_table.performApplicationPrelaunchCheck
        result = fn(pchAppKey)
        return result

    def getApplicationsTransitionStateNameFromEnum(self, state):
        "Returns a string for an application transition state"

        fn = self.function_table.getApplicationsTransitionStateNameFromEnum
        result = fn(state)
        return result

    def isQuitUserPromptRequested(self):
        "Returns true if the outgoing scene app has requested a save prompt before exiting"

        fn = self.function_table.isQuitUserPromptRequested
        result = fn()
        return result

    def launchInternalProcess(self, pchBinaryPath, pchArguments, pchWorkingDirectory):
        """
        Starts a subprocess within the calling application. This
        suppresses all application transition UI and automatically identifies the new executable 
        as part of the same application. On success the calling process should exit immediately. 
        If working directory is NULL or "" the directory portion of the binary path will be 
        the working directory.
        """

        fn = self.function_table.launchInternalProcess
        result = fn(pchBinaryPath, pchArguments, pchWorkingDirectory)
        return result

    def getCurrentSceneProcessId(self):
        """
        Returns the current scene process ID according to the application system. A scene process will get scene
        focus once it starts rendering, but it will appear here once it calls VR_Init with the Scene application
        type.
        """

        fn = self.function_table.getCurrentSceneProcessId
        result = fn()
        return result



class IVRChaperone_FnTable(Structure):
    _fields_ = [
        ("getCalibrationState", OPENVR_FNTABLE_CALLTYPE(ChaperoneCalibrationState)),
        ("getPlayAreaSize", OPENVR_FNTABLE_CALLTYPE(openvr_bool, POINTER(c_float), POINTER(c_float))),
        ("getPlayAreaRect", OPENVR_FNTABLE_CALLTYPE(openvr_bool, POINTER(HmdQuad_t))),
        ("reloadInfo", OPENVR_FNTABLE_CALLTYPE(None)),
        ("setSceneColor", OPENVR_FNTABLE_CALLTYPE(None, HmdColor_t)),
        ("getBoundsColor", OPENVR_FNTABLE_CALLTYPE(None, POINTER(HmdColor_t), c_int, c_float, POINTER(HmdColor_t))),
        ("areBoundsVisible", OPENVR_FNTABLE_CALLTYPE(openvr_bool)),
        ("forceBoundsVisible", OPENVR_FNTABLE_CALLTYPE(None, openvr_bool)),
    ]


class IVRChaperone(object):
    """
    HIGH LEVEL TRACKING SPACE ASSUMPTIONS:
    0,0,0 is the preferred standing area center.
    0Y is the floor height.
    -Z is the preferred forward facing direction.
    """

    def __init__(self):
        version_key = IVRChaperone_Version
        if not isInterfaceVersionValid(version_key):
            _checkInitError(VRInitError_Init_InterfaceNotFound)
        # Thank you lukexi https://github.com/lukexi/openvr-hs/blob/master/cbits/openvr_capi_helper.c#L9
        fn_key = b"FnTable:" + version_key
        fn_type = IVRChaperone_FnTable
        fn_table_ptr = cast(getGenericInterface(fn_key), POINTER(fn_type))
        if fn_table_ptr is None:
            raise OpenVRError("Error retrieving VR API for IVRChaperone")
        self.function_table = fn_table_ptr.contents

    def getCalibrationState(self):
        "Get the current state of Chaperone calibration. This state can change at any time during a session due to physical base station changes."

        fn = self.function_table.getCalibrationState
        result = fn()
        return result

    def getPlayAreaSize(self):
        """
        Returns the width and depth of the Play Area (formerly named Soft Bounds) in X and Z. 
        Tracking space center (0,0,0) is the center of the Play Area.
        """

        fn = self.function_table.getPlayAreaSize
        pSizeX = c_float()
        pSizeZ = c_float()
        result = fn(byref(pSizeX), byref(pSizeZ))
        return result, pSizeX.value, pSizeZ.value

    def getPlayAreaRect(self):
        """
        Returns the 4 corner positions of the Play Area (formerly named Soft Bounds).
        Corners are in counter-clockwise order.
        Standing center (0,0,0) is the center of the Play Area.
        It's a rectangle.
        2 sides are parallel to the X axis and 2 sides are parallel to the Z axis.
        Height of every corner is 0Y (on the floor).
        """

        fn = self.function_table.getPlayAreaRect
        rect = HmdQuad_t()
        result = fn(byref(rect))
        return result, rect

    def reloadInfo(self):
        "Reload Chaperone data from the .vrchap file on disk."

        fn = self.function_table.reloadInfo
        fn()

    def setSceneColor(self, color):
        "Optionally give the chaperone system a hit about the color and brightness in the scene"

        fn = self.function_table.setSceneColor
        fn(color)

    def getBoundsColor(self, nNumOutputColors, flCollisionBoundsFadeDistance):
        "Get the current chaperone bounds draw color and brightness"

        fn = self.function_table.getBoundsColor
        pOutputColorArray = HmdColor_t()
        pOutputCameraColor = HmdColor_t()
        fn(byref(pOutputColorArray), nNumOutputColors, flCollisionBoundsFadeDistance, byref(pOutputCameraColor))
        return pOutputColorArray, pOutputCameraColor

    def areBoundsVisible(self):
        "Determine whether the bounds are showing right now"

        fn = self.function_table.areBoundsVisible
        result = fn()
        return result

    def forceBoundsVisible(self, bForce):
        "Force the bounds to show, mostly for utilities"

        fn = self.function_table.forceBoundsVisible
        fn(bForce)



class IVRChaperoneSetup_FnTable(Structure):
    _fields_ = [
        ("commitWorkingCopy", OPENVR_FNTABLE_CALLTYPE(openvr_bool, EChaperoneConfigFile)),
        ("revertWorkingCopy", OPENVR_FNTABLE_CALLTYPE(None)),
        ("getWorkingPlayAreaSize", OPENVR_FNTABLE_CALLTYPE(openvr_bool, POINTER(c_float), POINTER(c_float))),
        ("getWorkingPlayAreaRect", OPENVR_FNTABLE_CALLTYPE(openvr_bool, POINTER(HmdQuad_t))),
        ("getWorkingCollisionBoundsInfo", OPENVR_FNTABLE_CALLTYPE(openvr_bool, POINTER(HmdQuad_t), POINTER(c_uint32))),
        ("getLiveCollisionBoundsInfo", OPENVR_FNTABLE_CALLTYPE(openvr_bool, POINTER(HmdQuad_t), POINTER(c_uint32))),
        ("getWorkingSeatedZeroPoseToRawTrackingPose", OPENVR_FNTABLE_CALLTYPE(openvr_bool, POINTER(HmdMatrix34_t))),
        ("getWorkingStandingZeroPoseToRawTrackingPose", OPENVR_FNTABLE_CALLTYPE(openvr_bool, POINTER(HmdMatrix34_t))),
        ("setWorkingPlayAreaSize", OPENVR_FNTABLE_CALLTYPE(None, c_float, c_float)),
        ("setWorkingCollisionBoundsInfo", OPENVR_FNTABLE_CALLTYPE(None, POINTER(HmdQuad_t), c_uint32)),
        ("setWorkingSeatedZeroPoseToRawTrackingPose", OPENVR_FNTABLE_CALLTYPE(None, POINTER(HmdMatrix34_t))),
        ("setWorkingStandingZeroPoseToRawTrackingPose", OPENVR_FNTABLE_CALLTYPE(None, POINTER(HmdMatrix34_t))),
        ("reloadFromDisk", OPENVR_FNTABLE_CALLTYPE(None, EChaperoneConfigFile)),
        ("getLiveSeatedZeroPoseToRawTrackingPose", OPENVR_FNTABLE_CALLTYPE(openvr_bool, POINTER(HmdMatrix34_t))),
        ("setWorkingCollisionBoundsTagsInfo", OPENVR_FNTABLE_CALLTYPE(None, POINTER(c_uint8), c_uint32)),
        ("getLiveCollisionBoundsTagsInfo", OPENVR_FNTABLE_CALLTYPE(openvr_bool, POINTER(c_uint8), POINTER(c_uint32))),
        ("setWorkingPhysicalBoundsInfo", OPENVR_FNTABLE_CALLTYPE(openvr_bool, POINTER(HmdQuad_t), c_uint32)),
        ("getLivePhysicalBoundsInfo", OPENVR_FNTABLE_CALLTYPE(openvr_bool, POINTER(HmdQuad_t), POINTER(c_uint32))),
        ("exportLiveToBuffer", OPENVR_FNTABLE_CALLTYPE(openvr_bool, c_char_p, POINTER(c_uint32))),
        ("importFromBufferToWorking", OPENVR_FNTABLE_CALLTYPE(openvr_bool, c_char_p, c_uint32)),
    ]


class IVRChaperoneSetup(object):
    """
    Manages the working copy of the chaperone info. By default this will be the same as the 
    live copy. Any changes made with this interface will stay in the working copy until 
    CommitWorkingCopy() is called, at which point the working copy and the live copy will be 
    the same again.
    """

    def __init__(self):
        version_key = IVRChaperoneSetup_Version
        if not isInterfaceVersionValid(version_key):
            _checkInitError(VRInitError_Init_InterfaceNotFound)
        # Thank you lukexi https://github.com/lukexi/openvr-hs/blob/master/cbits/openvr_capi_helper.c#L9
        fn_key = b"FnTable:" + version_key
        fn_type = IVRChaperoneSetup_FnTable
        fn_table_ptr = cast(getGenericInterface(fn_key), POINTER(fn_type))
        if fn_table_ptr is None:
            raise OpenVRError("Error retrieving VR API for IVRChaperoneSetup")
        self.function_table = fn_table_ptr.contents

    def commitWorkingCopy(self, configFile):
        "Saves the current working copy to disk"

        fn = self.function_table.commitWorkingCopy
        result = fn(configFile)
        return result

    def revertWorkingCopy(self):
        """
        Reverts the working copy to match the live chaperone calibration.
        To modify existing data this MUST be do WHILE getting a non-error ChaperoneCalibrationStatus.
        Only after this should you do gets and sets on the existing data.
        """

        fn = self.function_table.revertWorkingCopy
        fn()

    def getWorkingPlayAreaSize(self):
        """
        Returns the width and depth of the Play Area (formerly named Soft Bounds) in X and Z from the working copy.
        Tracking space center (0,0,0) is the center of the Play Area.
        """

        fn = self.function_table.getWorkingPlayAreaSize
        pSizeX = c_float()
        pSizeZ = c_float()
        result = fn(byref(pSizeX), byref(pSizeZ))
        return result, pSizeX.value, pSizeZ.value

    def getWorkingPlayAreaRect(self):
        """
        Returns the 4 corner positions of the Play Area (formerly named Soft Bounds) from the working copy.
        Corners are in clockwise order.
        Tracking space center (0,0,0) is the center of the Play Area.
        It's a rectangle.
        2 sides are parallel to the X axis and 2 sides are parallel to the Z axis.
        Height of every corner is 0Y (on the floor).
        """

        fn = self.function_table.getWorkingPlayAreaRect
        rect = HmdQuad_t()
        result = fn(byref(rect))
        return result, rect

    def getWorkingCollisionBoundsInfo(self):
        """
        Returns the number of Quads if the buffer points to null. Otherwise it returns Quads 
        into the buffer up to the max specified from the working copy.
        """

        fn = self.function_table.getWorkingCollisionBoundsInfo
        pQuadsBuffer = HmdQuad_t()
        punQuadsCount = c_uint32()
        result = fn(byref(pQuadsBuffer), byref(punQuadsCount))
        return result, pQuadsBuffer, punQuadsCount.value

    def getLiveCollisionBoundsInfo(self):
        """
        Returns the number of Quads if the buffer points to null. Otherwise it returns Quads 
        into the buffer up to the max specified.
        """

        fn = self.function_table.getLiveCollisionBoundsInfo
        pQuadsBuffer = HmdQuad_t()
        punQuadsCount = c_uint32()
        result = fn(byref(pQuadsBuffer), byref(punQuadsCount))
        return result, pQuadsBuffer, punQuadsCount.value

    def getWorkingSeatedZeroPoseToRawTrackingPose(self):
        "Returns the preferred seated position from the working copy."

        fn = self.function_table.getWorkingSeatedZeroPoseToRawTrackingPose
        pmatSeatedZeroPoseToRawTrackingPose = HmdMatrix34_t()
        result = fn(byref(pmatSeatedZeroPoseToRawTrackingPose))
        return result, pmatSeatedZeroPoseToRawTrackingPose

    def getWorkingStandingZeroPoseToRawTrackingPose(self):
        "Returns the standing origin from the working copy."

        fn = self.function_table.getWorkingStandingZeroPoseToRawTrackingPose
        pmatStandingZeroPoseToRawTrackingPose = HmdMatrix34_t()
        result = fn(byref(pmatStandingZeroPoseToRawTrackingPose))
        return result, pmatStandingZeroPoseToRawTrackingPose

    def setWorkingPlayAreaSize(self, sizeX, sizeZ):
        "Sets the Play Area in the working copy."

        fn = self.function_table.setWorkingPlayAreaSize
        fn(sizeX, sizeZ)

    def setWorkingCollisionBoundsInfo(self, unQuadsCount):
        "Sets the Collision Bounds in the working copy."

        fn = self.function_table.setWorkingCollisionBoundsInfo
        pQuadsBuffer = HmdQuad_t()
        fn(byref(pQuadsBuffer), unQuadsCount)
        return pQuadsBuffer

    def setWorkingSeatedZeroPoseToRawTrackingPose(self):
        "Sets the preferred seated position in the working copy."

        fn = self.function_table.setWorkingSeatedZeroPoseToRawTrackingPose
        pMatSeatedZeroPoseToRawTrackingPose = HmdMatrix34_t()
        fn(byref(pMatSeatedZeroPoseToRawTrackingPose))
        return pMatSeatedZeroPoseToRawTrackingPose

    def setWorkingStandingZeroPoseToRawTrackingPose(self):
        "Sets the preferred standing position in the working copy."

        fn = self.function_table.setWorkingStandingZeroPoseToRawTrackingPose
        pMatStandingZeroPoseToRawTrackingPose = HmdMatrix34_t()
        fn(byref(pMatStandingZeroPoseToRawTrackingPose))
        return pMatStandingZeroPoseToRawTrackingPose

    def reloadFromDisk(self, configFile):
        "Tear everything down and reload it from the file on disk"

        fn = self.function_table.reloadFromDisk
        fn(configFile)

    def getLiveSeatedZeroPoseToRawTrackingPose(self):
        "Returns the preferred seated position."

        fn = self.function_table.getLiveSeatedZeroPoseToRawTrackingPose
        pmatSeatedZeroPoseToRawTrackingPose = HmdMatrix34_t()
        result = fn(byref(pmatSeatedZeroPoseToRawTrackingPose))
        return result, pmatSeatedZeroPoseToRawTrackingPose

    def setWorkingCollisionBoundsTagsInfo(self, unTagCount):
        fn = self.function_table.setWorkingCollisionBoundsTagsInfo
        pTagsBuffer = c_uint8()
        fn(byref(pTagsBuffer), unTagCount)
        return pTagsBuffer.value

    def getLiveCollisionBoundsTagsInfo(self):
        fn = self.function_table.getLiveCollisionBoundsTagsInfo
        pTagsBuffer = c_uint8()
        punTagCount = c_uint32()
        result = fn(byref(pTagsBuffer), byref(punTagCount))
        return result, pTagsBuffer.value, punTagCount.value

    def setWorkingPhysicalBoundsInfo(self, unQuadsCount):
        fn = self.function_table.setWorkingPhysicalBoundsInfo
        pQuadsBuffer = HmdQuad_t()
        result = fn(byref(pQuadsBuffer), unQuadsCount)
        return result, pQuadsBuffer

    def getLivePhysicalBoundsInfo(self):
        fn = self.function_table.getLivePhysicalBoundsInfo
        pQuadsBuffer = HmdQuad_t()
        punQuadsCount = c_uint32()
        result = fn(byref(pQuadsBuffer), byref(punQuadsCount))
        return result, pQuadsBuffer, punQuadsCount.value

    def exportLiveToBuffer(self, pBuffer):
        fn = self.function_table.exportLiveToBuffer
        pnBufferLength = c_uint32()
        result = fn(pBuffer, byref(pnBufferLength))
        return result, pnBufferLength.value

    def importFromBufferToWorking(self, pBuffer, nImportFlags):
        fn = self.function_table.importFromBufferToWorking
        result = fn(pBuffer, nImportFlags)
        return result



class IVRCompositor_FnTable(Structure):
    _fields_ = [
        ("setTrackingSpace", OPENVR_FNTABLE_CALLTYPE(None, ETrackingUniverseOrigin)),
        ("getTrackingSpace", OPENVR_FNTABLE_CALLTYPE(ETrackingUniverseOrigin)),
        ("waitGetPoses", OPENVR_FNTABLE_CALLTYPE(EVRCompositorError, POINTER(TrackedDevicePose_t), c_uint32, POINTER(TrackedDevicePose_t), c_uint32)),
        ("getLastPoses", OPENVR_FNTABLE_CALLTYPE(EVRCompositorError, POINTER(TrackedDevicePose_t), c_uint32, POINTER(TrackedDevicePose_t), c_uint32)),
        ("getLastPoseForTrackedDeviceIndex", OPENVR_FNTABLE_CALLTYPE(EVRCompositorError, TrackedDeviceIndex_t, POINTER(TrackedDevicePose_t), POINTER(TrackedDevicePose_t))),
        ("submit", OPENVR_FNTABLE_CALLTYPE(EVRCompositorError, EVREye, POINTER(Texture_t), POINTER(VRTextureBounds_t), EVRSubmitFlags)),
        ("clearLastSubmittedFrame", OPENVR_FNTABLE_CALLTYPE(None)),
        ("postPresentHandoff", OPENVR_FNTABLE_CALLTYPE(None)),
        ("getFrameTiming", OPENVR_FNTABLE_CALLTYPE(openvr_bool, POINTER(Compositor_FrameTiming), c_uint32)),
        ("getFrameTimings", OPENVR_FNTABLE_CALLTYPE(c_uint32, POINTER(Compositor_FrameTiming), c_uint32)),
        ("getFrameTimeRemaining", OPENVR_FNTABLE_CALLTYPE(c_float)),
        ("getCumulativeStats", OPENVR_FNTABLE_CALLTYPE(None, POINTER(Compositor_CumulativeStats), c_uint32)),
        ("fadeToColor", OPENVR_FNTABLE_CALLTYPE(None, c_float, c_float, c_float, c_float, c_float, openvr_bool)),
        ("getCurrentFadeColor", OPENVR_FNTABLE_CALLTYPE(HmdColor_t, openvr_bool)),
        ("fadeGrid", OPENVR_FNTABLE_CALLTYPE(None, c_float, openvr_bool)),
        ("getCurrentGridAlpha", OPENVR_FNTABLE_CALLTYPE(c_float)),
        ("setSkyboxOverride", OPENVR_FNTABLE_CALLTYPE(EVRCompositorError, POINTER(Texture_t), c_uint32)),
        ("clearSkyboxOverride", OPENVR_FNTABLE_CALLTYPE(None)),
        ("compositorBringToFront", OPENVR_FNTABLE_CALLTYPE(None)),
        ("compositorGoToBack", OPENVR_FNTABLE_CALLTYPE(None)),
        ("compositorQuit", OPENVR_FNTABLE_CALLTYPE(None)),
        ("isFullscreen", OPENVR_FNTABLE_CALLTYPE(openvr_bool)),
        ("getCurrentSceneFocusProcess", OPENVR_FNTABLE_CALLTYPE(c_uint32)),
        ("getLastFrameRenderer", OPENVR_FNTABLE_CALLTYPE(c_uint32)),
        ("canRenderScene", OPENVR_FNTABLE_CALLTYPE(openvr_bool)),
        ("showMirrorWindow", OPENVR_FNTABLE_CALLTYPE(None)),
        ("hideMirrorWindow", OPENVR_FNTABLE_CALLTYPE(None)),
        ("isMirrorWindowVisible", OPENVR_FNTABLE_CALLTYPE(openvr_bool)),
        ("compositorDumpImages", OPENVR_FNTABLE_CALLTYPE(None)),
        ("shouldAppRenderWithLowResources", OPENVR_FNTABLE_CALLTYPE(openvr_bool)),
        ("forceInterleavedReprojectionOn", OPENVR_FNTABLE_CALLTYPE(None, openvr_bool)),
        ("forceReconnectProcess", OPENVR_FNTABLE_CALLTYPE(None)),
        ("suspendRendering", OPENVR_FNTABLE_CALLTYPE(None, openvr_bool)),
        ("getMirrorTextureD3D11", OPENVR_FNTABLE_CALLTYPE(EVRCompositorError, EVREye, c_void_p, POINTER(c_void_p))),
        ("releaseMirrorTextureD3D11", OPENVR_FNTABLE_CALLTYPE(None, c_void_p)),
        ("getMirrorTextureGL", OPENVR_FNTABLE_CALLTYPE(EVRCompositorError, EVREye, POINTER(glUInt_t), POINTER(glSharedTextureHandle_t))),
        ("releaseSharedGLTexture", OPENVR_FNTABLE_CALLTYPE(openvr_bool, glUInt_t, glSharedTextureHandle_t)),
        ("lockGLSharedTextureForAccess", OPENVR_FNTABLE_CALLTYPE(None, glSharedTextureHandle_t)),
        ("unlockGLSharedTextureForAccess", OPENVR_FNTABLE_CALLTYPE(None, glSharedTextureHandle_t)),
        ("getVulkanInstanceExtensionsRequired", OPENVR_FNTABLE_CALLTYPE(c_uint32, c_char_p, c_uint32)),
        ("getVulkanDeviceExtensionsRequired", OPENVR_FNTABLE_CALLTYPE(c_uint32, POINTER(VkPhysicalDevice_T), c_char_p, c_uint32)),
    ]


class IVRCompositor(object):
    "Allows the application to interact with the compositor"

    def __init__(self):
        version_key = IVRCompositor_Version
        if not isInterfaceVersionValid(version_key):
            _checkInitError(VRInitError_Init_InterfaceNotFound)
        # Thank you lukexi https://github.com/lukexi/openvr-hs/blob/master/cbits/openvr_capi_helper.c#L9
        fn_key = b"FnTable:" + version_key
        fn_type = IVRCompositor_FnTable
        fn_table_ptr = cast(getGenericInterface(fn_key), POINTER(fn_type))
        if fn_table_ptr is None:
            raise OpenVRError("Error retrieving VR API for IVRCompositor")
        self.function_table = fn_table_ptr.contents

    def setTrackingSpace(self, eOrigin):
        "Sets tracking space returned by WaitGetPoses"

        fn = self.function_table.setTrackingSpace
        fn(eOrigin)

    def getTrackingSpace(self):
        "Gets current tracking space returned by WaitGetPoses"

        fn = self.function_table.getTrackingSpace
        result = fn()
        return result

    def waitGetPoses(self, pRenderPoseArray, unRenderPoseArrayCount, pGamePoseArray, unGamePoseArrayCount):
        """
        Scene applications should call this function to get poses to render with (and optionally poses predicted an additional frame out to use for gameplay).
        This function will block until "running start" milliseconds before the start of the frame, and should be called at the last moment before needing to
        start rendering.
        * Return codes:
        - IsNotSceneApplication (make sure to call VR_Init with VRApplicaiton_Scene)
        - DoNotHaveFocus (some other app has taken focus - this will throttle the call to 10hz to reduce the impact on that app)
        """

        fn = self.function_table.waitGetPoses
        # TODO: Automate this manual translation
        # Convert non-pointer python arguments to pointers
        if pRenderPoseArray is not None:
            pRenderPoseArray = byref(pRenderPoseArray[0])
        if pGamePoseArray is not None:
            pGamePoseArray = byref(pGamePoseArray[0])
        result = fn(pRenderPoseArray, unRenderPoseArrayCount, pGamePoseArray, unGamePoseArrayCount)
        return result

    def getLastPoses(self, unRenderPoseArrayCount, unGamePoseArrayCount):
        "Get the last set of poses returned by WaitGetPoses."

        fn = self.function_table.getLastPoses
        pRenderPoseArray = TrackedDevicePose_t()
        pGamePoseArray = TrackedDevicePose_t()
        result = fn(byref(pRenderPoseArray), unRenderPoseArrayCount, byref(pGamePoseArray), unGamePoseArrayCount)
        return result, pRenderPoseArray, pGamePoseArray

    def getLastPoseForTrackedDeviceIndex(self, unDeviceIndex):
        """
        Interface for accessing last set of poses returned by WaitGetPoses one at a time.
        Returns VRCompositorError_IndexOutOfRange if unDeviceIndex not less than k_unMaxTrackedDeviceCount otherwise VRCompositorError_None.
        It is okay to pass NULL for either pose if you only want one of the values.
        """

        fn = self.function_table.getLastPoseForTrackedDeviceIndex
        pOutputPose = TrackedDevicePose_t()
        pOutputGamePose = TrackedDevicePose_t()
        result = fn(unDeviceIndex, byref(pOutputPose), byref(pOutputGamePose))
        return result, pOutputPose, pOutputGamePose

    def submit(self, eEye, pTexture, pBounds=None, nSubmitFlags=Submit_Default):
        """
        Updated scene texture to display. If pBounds is NULL the entire texture will be used.  If called from an OpenGL app, consider adding a glFlush after
        Submitting both frames to signal the driver to start processing, otherwise it may wait until the command buffer fills up, causing the app to miss frames.
        * OpenGL dirty state:
        glBindTexture
        * Return codes:
        - IsNotSceneApplication (make sure to call VR_Init with VRApplicaiton_Scene)
        - DoNotHaveFocus (some other app has taken focus)
        - TextureIsOnWrongDevice (application did not use proper AdapterIndex - see IVRSystem.GetDXGIOutputInfo)
        - SharedTexturesNotSupported (application needs to call CreateDXGIFactory1 or later before creating DX device)
        - TextureUsesUnsupportedFormat (scene textures must be compatible with DXGI sharing rules - e.g. uncompressed, no mips, etc.)
        - InvalidTexture (usually means bad arguments passed in)
        - AlreadySubmitted (app has submitted two left textures or two right textures in a single frame - i.e. before calling WaitGetPoses again)
        """

        fn = self.function_table.submit
        # TODO: Automate this manual translation
        eError = fn(eEye, byref(pTexture), pBounds, nSubmitFlags)
        return eError

    def clearLastSubmittedFrame(self):
        """
        Clears the frame that was sent with the last call to Submit. This will cause the 
        compositor to show the grid until Submit is called again.
        """

        fn = self.function_table.clearLastSubmittedFrame
        fn()

    def postPresentHandoff(self):
        """
        Call immediately after presenting your app's window (i.e. companion window) to unblock the compositor.
        This is an optional call, which only needs to be used if you can't instead call WaitGetPoses immediately after Present.
        For example, if your engine's render and game loop are not on separate threads, or blocking the render thread until 3ms before the next vsync would
        introduce a deadlock of some sort.  This function tells the compositor that you have finished all rendering after having Submitted buffers for both
        eyes, and it is free to start its rendering work.  This should only be called from the same thread you are rendering on.
        """

        fn = self.function_table.postPresentHandoff
        fn()

    def getFrameTiming(self, unFramesAgo):
        """
        Returns true if timing data is filled it.  Sets oldest timing info if nFramesAgo is larger than the stored history.
        Be sure to set timing.size = sizeof(Compositor_FrameTiming) on struct passed in before calling this function.
        """

        fn = self.function_table.getFrameTiming
        pTiming = Compositor_FrameTiming()
        result = fn(byref(pTiming), unFramesAgo)
        return result, pTiming

    def getFrameTimings(self, nFrames):
        """
        Interface for copying a range of timing data.  Frames are returned in ascending order (oldest to newest) with the last being the most recent frame.
        Only the first entry's m_nSize needs to be set, as the rest will be inferred from that.  Returns total number of entries filled out.
        """

        fn = self.function_table.getFrameTimings
        pTiming = Compositor_FrameTiming()
        result = fn(byref(pTiming), nFrames)
        return result, pTiming

    def getFrameTimeRemaining(self):
        """
        Returns the time in seconds left in the current (as identified by FrameTiming's frameIndex) frame.
        Due to "running start", this value may roll over to the next frame before ever reaching 0.0.
        """

        fn = self.function_table.getFrameTimeRemaining
        result = fn()
        return result

    def getCumulativeStats(self, nStatsSizeInBytes):
        "Fills out stats accumulated for the last connected application.  Pass in sizeof( Compositor_CumulativeStats ) as second parameter."

        fn = self.function_table.getCumulativeStats
        pStats = Compositor_CumulativeStats()
        fn(byref(pStats), nStatsSizeInBytes)
        return pStats

    def fadeToColor(self, fSeconds, fRed, fGreen, fBlue, fAlpha, bBackground):
        """
        Fades the view on the HMD to the specified color. The fade will take fSeconds, and the color values are between
        0.0 and 1.0. This color is faded on top of the scene based on the alpha parameter. Removing the fade color instantly 
        would be FadeToColor( 0.0, 0.0, 0.0, 0.0, 0.0 ).  Values are in un-premultiplied alpha space.
        """

        fn = self.function_table.fadeToColor
        fn(fSeconds, fRed, fGreen, fBlue, fAlpha, bBackground)

    def getCurrentFadeColor(self, bBackground):
        "Get current fade color value."

        fn = self.function_table.getCurrentFadeColor
        result = fn(bBackground)
        return result

    def fadeGrid(self, fSeconds, bFadeIn):
        "Fading the Grid in or out in fSeconds"

        fn = self.function_table.fadeGrid
        fn(fSeconds, bFadeIn)

    def getCurrentGridAlpha(self):
        "Get current alpha value of grid."

        fn = self.function_table.getCurrentGridAlpha
        result = fn()
        return result

    def setSkyboxOverride(self, unTextureCount):
        """
        Override the skybox used in the compositor (e.g. for during level loads when the app can't feed scene images fast enough)
        Order is Front, Back, Left, Right, Top, Bottom.  If only a single texture is passed, it is assumed in lat-long format.
        If two are passed, it is assumed a lat-long stereo pair.
        """

        fn = self.function_table.setSkyboxOverride
        pTextures = Texture_t()
        result = fn(byref(pTextures), unTextureCount)
        return result, pTextures

    def clearSkyboxOverride(self):
        "Resets compositor skybox back to defaults."

        fn = self.function_table.clearSkyboxOverride
        fn()

    def compositorBringToFront(self):
        """
        Brings the compositor window to the front. This is useful for covering any other window that may be on the HMD
        and is obscuring the compositor window.
        """

        fn = self.function_table.compositorBringToFront
        fn()

    def compositorGoToBack(self):
        "Pushes the compositor window to the back. This is useful for allowing other applications to draw directly to the HMD."

        fn = self.function_table.compositorGoToBack
        fn()

    def compositorQuit(self):
        """
        Tells the compositor process to clean up and exit. You do not need to call this function at shutdown. Under normal 
        circumstances the compositor will manage its own life cycle based on what applications are running.
        """

        fn = self.function_table.compositorQuit
        fn()

    def isFullscreen(self):
        "Return whether the compositor is fullscreen"

        fn = self.function_table.isFullscreen
        result = fn()
        return result

    def getCurrentSceneFocusProcess(self):
        "Returns the process ID of the process that is currently rendering the scene"

        fn = self.function_table.getCurrentSceneFocusProcess
        result = fn()
        return result

    def getLastFrameRenderer(self):
        """
        Returns the process ID of the process that rendered the last frame (or 0 if the compositor itself rendered the frame.)
        Returns 0 when fading out from an app and the app's process Id when fading into an app.
        """

        fn = self.function_table.getLastFrameRenderer
        result = fn()
        return result

    def canRenderScene(self):
        "Returns true if the current process has the scene focus"

        fn = self.function_table.canRenderScene
        result = fn()
        return result

    def showMirrorWindow(self):
        "Creates a window on the primary monitor to display what is being shown in the headset."

        fn = self.function_table.showMirrorWindow
        fn()

    def hideMirrorWindow(self):
        "Closes the mirror window."

        fn = self.function_table.hideMirrorWindow
        fn()

    def isMirrorWindowVisible(self):
        "Returns true if the mirror window is shown."

        fn = self.function_table.isMirrorWindowVisible
        result = fn()
        return result

    def compositorDumpImages(self):
        "Writes all images that the compositor knows about (including overlays) to a 'screenshots' folder in the SteamVR runtime root."

        fn = self.function_table.compositorDumpImages
        fn()

    def shouldAppRenderWithLowResources(self):
        "Let an app know it should be rendering with low resources."

        fn = self.function_table.shouldAppRenderWithLowResources
        result = fn()
        return result

    def forceInterleavedReprojectionOn(self, bOverride):
        "Override interleaved reprojection logic to force on."

        fn = self.function_table.forceInterleavedReprojectionOn
        fn(bOverride)

    def forceReconnectProcess(self):
        "Force reconnecting to the compositor process."

        fn = self.function_table.forceReconnectProcess
        fn()

    def suspendRendering(self, bSuspend):
        "Temporarily suspends rendering (useful for finer control over scene transitions)."

        fn = self.function_table.suspendRendering
        fn(bSuspend)

    def getMirrorTextureD3D11(self, eEye, pD3D11DeviceOrResource):
        """
        Opens a shared D3D11 texture with the undistorted composited image for each eye.  Use ReleaseMirrorTextureD3D11 when finished
        instead of calling Release on the resource itself.
        """

        fn = self.function_table.getMirrorTextureD3D11
        ppD3D11ShaderResourceView = c_void_p()
        result = fn(eEye, pD3D11DeviceOrResource, byref(ppD3D11ShaderResourceView))
        return result, ppD3D11ShaderResourceView.value

    def releaseMirrorTextureD3D11(self, pD3D11ShaderResourceView):
        fn = self.function_table.releaseMirrorTextureD3D11
        fn(pD3D11ShaderResourceView)

    def getMirrorTextureGL(self, eEye):
        "Access to mirror textures from OpenGL."

        fn = self.function_table.getMirrorTextureGL
        pglTextureId = glUInt_t()
        pglSharedTextureHandle = glSharedTextureHandle_t()
        result = fn(eEye, byref(pglTextureId), byref(pglSharedTextureHandle))
        return result, pglTextureId, pglSharedTextureHandle

    def releaseSharedGLTexture(self, glTextureId, glSharedTextureHandle):
        fn = self.function_table.releaseSharedGLTexture
        result = fn(glTextureId, glSharedTextureHandle)
        return result

    def lockGLSharedTextureForAccess(self, glSharedTextureHandle):
        fn = self.function_table.lockGLSharedTextureForAccess
        fn(glSharedTextureHandle)

    def unlockGLSharedTextureForAccess(self, glSharedTextureHandle):
        fn = self.function_table.unlockGLSharedTextureForAccess
        fn(glSharedTextureHandle)

    def getVulkanInstanceExtensionsRequired(self, pchValue, unBufferSize):
        """
        [Vulkan Only]
        return 0. Otherwise it returns the length of the number of bytes necessary to hold this string including the trailing
        null.  The string will be a space separated list of-required instance extensions to enable in VkCreateInstance
        """

        fn = self.function_table.getVulkanInstanceExtensionsRequired
        result = fn(pchValue, unBufferSize)
        return result

    def getVulkanDeviceExtensionsRequired(self, pchValue, unBufferSize):
        """
        [Vulkan only]
        return 0. Otherwise it returns the length of the number of bytes necessary to hold this string including the trailing
        null.  The string will be a space separated list of required device extensions to enable in VkCreateDevice
        """

        fn = self.function_table.getVulkanDeviceExtensionsRequired
        pPhysicalDevice = VkPhysicalDevice_T()
        result = fn(byref(pPhysicalDevice), pchValue, unBufferSize)
        return result, pPhysicalDevice



class IVROverlay_FnTable(Structure):
    _fields_ = [
        ("findOverlay", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, c_char_p, POINTER(VROverlayHandle_t))),
        ("createOverlay", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, c_char_p, c_char_p, POINTER(VROverlayHandle_t))),
        ("destroyOverlay", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t)),
        ("setHighQualityOverlay", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t)),
        ("getHighQualityOverlay", OPENVR_FNTABLE_CALLTYPE(VROverlayHandle_t)),
        ("getOverlayKey", OPENVR_FNTABLE_CALLTYPE(c_uint32, VROverlayHandle_t, c_char_p, c_uint32, POINTER(EVROverlayError))),
        ("getOverlayName", OPENVR_FNTABLE_CALLTYPE(c_uint32, VROverlayHandle_t, c_char_p, c_uint32, POINTER(EVROverlayError))),
        ("setOverlayName", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, c_char_p)),
        ("getOverlayImageData", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, c_void_p, c_uint32, POINTER(c_uint32), POINTER(c_uint32))),
        ("getOverlayErrorNameFromEnum", OPENVR_FNTABLE_CALLTYPE(c_char_p, EVROverlayError)),
        ("setOverlayRenderingPid", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, c_uint32)),
        ("getOverlayRenderingPid", OPENVR_FNTABLE_CALLTYPE(c_uint32, VROverlayHandle_t)),
        ("setOverlayFlag", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, VROverlayFlags, openvr_bool)),
        ("getOverlayFlag", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, VROverlayFlags, POINTER(openvr_bool))),
        ("setOverlayColor", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, c_float, c_float, c_float)),
        ("getOverlayColor", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, POINTER(c_float), POINTER(c_float), POINTER(c_float))),
        ("setOverlayAlpha", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, c_float)),
        ("getOverlayAlpha", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, POINTER(c_float))),
        ("setOverlayTexelAspect", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, c_float)),
        ("getOverlayTexelAspect", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, POINTER(c_float))),
        ("setOverlaySortOrder", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, c_uint32)),
        ("getOverlaySortOrder", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, POINTER(c_uint32))),
        ("setOverlayWidthInMeters", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, c_float)),
        ("getOverlayWidthInMeters", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, POINTER(c_float))),
        ("setOverlayAutoCurveDistanceRangeInMeters", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, c_float, c_float)),
        ("getOverlayAutoCurveDistanceRangeInMeters", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, POINTER(c_float), POINTER(c_float))),
        ("setOverlayTextureColorSpace", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, EColorSpace)),
        ("getOverlayTextureColorSpace", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, POINTER(EColorSpace))),
        ("setOverlayTextureBounds", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, POINTER(VRTextureBounds_t))),
        ("getOverlayTextureBounds", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, POINTER(VRTextureBounds_t))),
        ("getOverlayRenderModel", OPENVR_FNTABLE_CALLTYPE(c_uint32, VROverlayHandle_t, c_char_p, c_uint32, POINTER(HmdColor_t), POINTER(EVROverlayError))),
        ("setOverlayRenderModel", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, c_char_p, POINTER(HmdColor_t))),
        ("getOverlayTransformType", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, POINTER(VROverlayTransformType))),
        ("setOverlayTransformAbsolute", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, ETrackingUniverseOrigin, POINTER(HmdMatrix34_t))),
        ("getOverlayTransformAbsolute", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, POINTER(ETrackingUniverseOrigin), POINTER(HmdMatrix34_t))),
        ("setOverlayTransformTrackedDeviceRelative", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, TrackedDeviceIndex_t, POINTER(HmdMatrix34_t))),
        ("getOverlayTransformTrackedDeviceRelative", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, POINTER(TrackedDeviceIndex_t), POINTER(HmdMatrix34_t))),
        ("setOverlayTransformTrackedDeviceComponent", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, TrackedDeviceIndex_t, c_char_p)),
        ("getOverlayTransformTrackedDeviceComponent", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, POINTER(TrackedDeviceIndex_t), c_char_p, c_uint32)),
        ("getOverlayTransformOverlayRelative", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, POINTER(VROverlayHandle_t), POINTER(HmdMatrix34_t))),
        ("setOverlayTransformOverlayRelative", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, VROverlayHandle_t, POINTER(HmdMatrix34_t))),
        ("showOverlay", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t)),
        ("hideOverlay", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t)),
        ("isOverlayVisible", OPENVR_FNTABLE_CALLTYPE(openvr_bool, VROverlayHandle_t)),
        ("getTransformForOverlayCoordinates", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, ETrackingUniverseOrigin, HmdVector2_t, POINTER(HmdMatrix34_t))),
        ("pollNextOverlayEvent", OPENVR_FNTABLE_CALLTYPE(openvr_bool, VROverlayHandle_t, POINTER(VREvent_t), c_uint32)),
        ("getOverlayInputMethod", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, POINTER(VROverlayInputMethod))),
        ("setOverlayInputMethod", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, VROverlayInputMethod)),
        ("getOverlayMouseScale", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, POINTER(HmdVector2_t))),
        ("setOverlayMouseScale", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, POINTER(HmdVector2_t))),
        ("computeOverlayIntersection", OPENVR_FNTABLE_CALLTYPE(openvr_bool, VROverlayHandle_t, POINTER(VROverlayIntersectionParams_t), POINTER(VROverlayIntersectionResults_t))),
        ("handleControllerOverlayInteractionAsMouse", OPENVR_FNTABLE_CALLTYPE(openvr_bool, VROverlayHandle_t, TrackedDeviceIndex_t)),
        ("isHoverTargetOverlay", OPENVR_FNTABLE_CALLTYPE(openvr_bool, VROverlayHandle_t)),
        ("getGamepadFocusOverlay", OPENVR_FNTABLE_CALLTYPE(VROverlayHandle_t)),
        ("setGamepadFocusOverlay", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t)),
        ("setOverlayNeighbor", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, EOverlayDirection, VROverlayHandle_t, VROverlayHandle_t)),
        ("moveGamepadFocusToNeighbor", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, EOverlayDirection, VROverlayHandle_t)),
        ("setOverlayTexture", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, POINTER(Texture_t))),
        ("clearOverlayTexture", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t)),
        ("setOverlayRaw", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, c_void_p, c_uint32, c_uint32, c_uint32)),
        ("setOverlayFromFile", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, c_char_p)),
        ("getOverlayTexture", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, POINTER(c_void_p), c_void_p, POINTER(c_uint32), POINTER(c_uint32), POINTER(c_uint32), POINTER(ETextureType), POINTER(EColorSpace), POINTER(VRTextureBounds_t))),
        ("releaseNativeOverlayHandle", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, c_void_p)),
        ("getOverlayTextureSize", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, POINTER(c_uint32), POINTER(c_uint32))),
        ("createDashboardOverlay", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, c_char_p, c_char_p, POINTER(VROverlayHandle_t), POINTER(VROverlayHandle_t))),
        ("isDashboardVisible", OPENVR_FNTABLE_CALLTYPE(openvr_bool)),
        ("isActiveDashboardOverlay", OPENVR_FNTABLE_CALLTYPE(openvr_bool, VROverlayHandle_t)),
        ("setDashboardOverlaySceneProcess", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, c_uint32)),
        ("getDashboardOverlaySceneProcess", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, POINTER(c_uint32))),
        ("showDashboard", OPENVR_FNTABLE_CALLTYPE(None, c_char_p)),
        ("getPrimaryDashboardDevice", OPENVR_FNTABLE_CALLTYPE(TrackedDeviceIndex_t)),
        ("showKeyboard", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, EGamepadTextInputMode, EGamepadTextInputLineMode, c_char_p, c_uint32, c_char_p, openvr_bool, c_uint64)),
        ("showKeyboardForOverlay", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, EGamepadTextInputMode, EGamepadTextInputLineMode, c_char_p, c_uint32, c_char_p, openvr_bool, c_uint64)),
        ("getKeyboardText", OPENVR_FNTABLE_CALLTYPE(c_uint32, c_char_p, c_uint32)),
        ("hideKeyboard", OPENVR_FNTABLE_CALLTYPE(None)),
        ("setKeyboardTransformAbsolute", OPENVR_FNTABLE_CALLTYPE(None, ETrackingUniverseOrigin, POINTER(HmdMatrix34_t))),
        ("setKeyboardPositionForOverlay", OPENVR_FNTABLE_CALLTYPE(None, VROverlayHandle_t, HmdRect2_t)),
        ("setOverlayIntersectionMask", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, POINTER(VROverlayIntersectionMaskPrimitive_t), c_uint32, c_uint32)),
        ("getOverlayFlags", OPENVR_FNTABLE_CALLTYPE(EVROverlayError, VROverlayHandle_t, POINTER(c_uint32))),
        ("showMessageOverlay", OPENVR_FNTABLE_CALLTYPE(VRMessageOverlayResponse, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p)),
    ]


class IVROverlay(object):
    def __init__(self):
        version_key = IVROverlay_Version
        if not isInterfaceVersionValid(version_key):
            _checkInitError(VRInitError_Init_InterfaceNotFound)
        # Thank you lukexi https://github.com/lukexi/openvr-hs/blob/master/cbits/openvr_capi_helper.c#L9
        fn_key = b"FnTable:" + version_key
        fn_type = IVROverlay_FnTable
        fn_table_ptr = cast(getGenericInterface(fn_key), POINTER(fn_type))
        if fn_table_ptr is None:
            raise OpenVRError("Error retrieving VR API for IVROverlay")
        self.function_table = fn_table_ptr.contents

    def findOverlay(self, pchOverlayKey):
        "Finds an existing overlay with the specified key."

        fn = self.function_table.findOverlay
        pOverlayHandle = VROverlayHandle_t()
        result = fn(pchOverlayKey, byref(pOverlayHandle))
        return result, pOverlayHandle

    def createOverlay(self, pchOverlayKey, pchOverlayName):
        "Creates a new named overlay. All overlays start hidden and with default settings."

        fn = self.function_table.createOverlay
        pOverlayHandle = VROverlayHandle_t()
        result = fn(pchOverlayKey, pchOverlayName, byref(pOverlayHandle))
        return result, pOverlayHandle

    def destroyOverlay(self, ulOverlayHandle):
        """
        Destroys the specified overlay. When an application calls VR_Shutdown all overlays created by that app are
        automatically destroyed.
        """

        fn = self.function_table.destroyOverlay
        result = fn(ulOverlayHandle)
        return result

    def setHighQualityOverlay(self, ulOverlayHandle):
        """
        Specify which overlay to use the high quality render path.  This overlay will be composited in during the distortion pass which
        results in it drawing on top of everything else, but also at a higher quality as it samples the source texture directly rather than
        rasterizing into each eye's render texture first.  Because if this, only one of these is supported at any given time.  It is most useful
        for overlays that are expected to take up most of the user's view (e.g. streaming video).
        This mode does not support mouse input to your overlay.
        """

        fn = self.function_table.setHighQualityOverlay
        result = fn(ulOverlayHandle)
        return result

    def getHighQualityOverlay(self):
        """
        Returns the overlay handle of the current overlay being rendered using the single high quality overlay render path.
        Otherwise it will return k_ulOverlayHandleInvalid.
        """

        fn = self.function_table.getHighQualityOverlay
        result = fn()
        return result

    def getOverlayKey(self, ulOverlayHandle, pchValue, unBufferSize):
        """
        Fills the provided buffer with the string key of the overlay. Returns the size of buffer required to store the key, including
        the terminating null character. k_unVROverlayMaxKeyLength will be enough bytes to fit the string.
        """

        fn = self.function_table.getOverlayKey
        pError = EVROverlayError()
        result = fn(ulOverlayHandle, pchValue, unBufferSize, byref(pError))
        return result, pError

    def getOverlayName(self, ulOverlayHandle, pchValue, unBufferSize):
        """
        Fills the provided buffer with the friendly name of the overlay. Returns the size of buffer required to store the key, including
        the terminating null character. k_unVROverlayMaxNameLength will be enough bytes to fit the string.
        """

        fn = self.function_table.getOverlayName
        pError = EVROverlayError()
        result = fn(ulOverlayHandle, pchValue, unBufferSize, byref(pError))
        return result, pError

    def setOverlayName(self, ulOverlayHandle, pchName):
        "set the name to use for this overlay"

        fn = self.function_table.setOverlayName
        result = fn(ulOverlayHandle, pchName)
        return result

    def getOverlayImageData(self, ulOverlayHandle, pvBuffer, unBufferSize):
        """
        Gets the raw image data from an overlay. Overlay image data is always returned as RGBA data, 4 bytes per pixel. If the buffer is not large enough, width and height 
        will be set and VROverlayError_ArrayTooSmall is returned.
        """

        fn = self.function_table.getOverlayImageData
        punWidth = c_uint32()
        punHeight = c_uint32()
        result = fn(ulOverlayHandle, pvBuffer, unBufferSize, byref(punWidth), byref(punHeight))
        return result, punWidth.value, punHeight.value

    def getOverlayErrorNameFromEnum(self, error):
        """
        returns a string that corresponds with the specified overlay error. The string will be the name 
        of the error enum value for all valid error codes
        """

        fn = self.function_table.getOverlayErrorNameFromEnum
        result = fn(error)
        return result

    def setOverlayRenderingPid(self, ulOverlayHandle, unPID):
        """
        Sets the pid that is allowed to render to this overlay (the creator pid is always allow to render),
        by default this is the pid of the process that made the overlay
        """

        fn = self.function_table.setOverlayRenderingPid
        result = fn(ulOverlayHandle, unPID)
        return result

    def getOverlayRenderingPid(self, ulOverlayHandle):
        "Gets the pid that is allowed to render to this overlay"

        fn = self.function_table.getOverlayRenderingPid
        result = fn(ulOverlayHandle)
        return result

    def setOverlayFlag(self, ulOverlayHandle, eOverlayFlag, bEnabled):
        "Specify flag setting for a given overlay"

        fn = self.function_table.setOverlayFlag
        result = fn(ulOverlayHandle, eOverlayFlag, bEnabled)
        return result

    def getOverlayFlag(self, ulOverlayHandle, eOverlayFlag):
        "Sets flag setting for a given overlay"

        fn = self.function_table.getOverlayFlag
        pbEnabled = openvr_bool()
        result = fn(ulOverlayHandle, eOverlayFlag, byref(pbEnabled))
        return result, pbEnabled

    def setOverlayColor(self, ulOverlayHandle, fRed, fGreen, fBlue):
        "Sets the color tint of the overlay quad. Use 0.0 to 1.0 per channel."

        fn = self.function_table.setOverlayColor
        result = fn(ulOverlayHandle, fRed, fGreen, fBlue)
        return result

    def getOverlayColor(self, ulOverlayHandle):
        "Gets the color tint of the overlay quad."

        fn = self.function_table.getOverlayColor
        pfRed = c_float()
        pfGreen = c_float()
        pfBlue = c_float()
        result = fn(ulOverlayHandle, byref(pfRed), byref(pfGreen), byref(pfBlue))
        return result, pfRed.value, pfGreen.value, pfBlue.value

    def setOverlayAlpha(self, ulOverlayHandle, fAlpha):
        "Sets the alpha of the overlay quad. Use 1.0 for 100 percent opacity to 0.0 for 0 percent opacity."

        fn = self.function_table.setOverlayAlpha
        result = fn(ulOverlayHandle, fAlpha)
        return result

    def getOverlayAlpha(self, ulOverlayHandle):
        "Gets the alpha of the overlay quad. By default overlays are rendering at 100 percent alpha (1.0)."

        fn = self.function_table.getOverlayAlpha
        pfAlpha = c_float()
        result = fn(ulOverlayHandle, byref(pfAlpha))
        return result, pfAlpha.value

    def setOverlayTexelAspect(self, ulOverlayHandle, fTexelAspect):
        """
        Sets the aspect ratio of the texels in the overlay. 1.0 means the texels are square. 2.0 means the texels
        are twice as wide as they are tall. Defaults to 1.0.
        """

        fn = self.function_table.setOverlayTexelAspect
        result = fn(ulOverlayHandle, fTexelAspect)
        return result

    def getOverlayTexelAspect(self, ulOverlayHandle):
        "Gets the aspect ratio of the texels in the overlay. Defaults to 1.0"

        fn = self.function_table.getOverlayTexelAspect
        pfTexelAspect = c_float()
        result = fn(ulOverlayHandle, byref(pfTexelAspect))
        return result, pfTexelAspect.value

    def setOverlaySortOrder(self, ulOverlayHandle, unSortOrder):
        """
        Sets the rendering sort order for the overlay. Overlays are rendered this order:
             Overlays owned by the scene application
             Overlays owned by some other application
        *	Within a category overlays are rendered lowest sort order to highest sort order. Overlays with the same 
        sort order are rendered back to front base on distance from the HMD.
        *	Sort order defaults to 0.
        """

        fn = self.function_table.setOverlaySortOrder
        result = fn(ulOverlayHandle, unSortOrder)
        return result

    def getOverlaySortOrder(self, ulOverlayHandle):
        "Gets the sort order of the overlay. See SetOverlaySortOrder for how this works."

        fn = self.function_table.getOverlaySortOrder
        punSortOrder = c_uint32()
        result = fn(ulOverlayHandle, byref(punSortOrder))
        return result, punSortOrder.value

    def setOverlayWidthInMeters(self, ulOverlayHandle, fWidthInMeters):
        "Sets the width of the overlay quad in meters. By default overlays are rendered on a quad that is 1 meter across"

        fn = self.function_table.setOverlayWidthInMeters
        result = fn(ulOverlayHandle, fWidthInMeters)
        return result

    def getOverlayWidthInMeters(self, ulOverlayHandle):
        "Returns the width of the overlay quad in meters. By default overlays are rendered on a quad that is 1 meter across"

        fn = self.function_table.getOverlayWidthInMeters
        pfWidthInMeters = c_float()
        result = fn(ulOverlayHandle, byref(pfWidthInMeters))
        return result, pfWidthInMeters.value

    def setOverlayAutoCurveDistanceRangeInMeters(self, ulOverlayHandle, fMinDistanceInMeters, fMaxDistanceInMeters):
        """
        For high-quality curved overlays only, sets the distance range in meters from the overlay used to automatically curve
        the surface around the viewer.  Min is distance is when the surface will be most curved.  Max is when least curved.
        """

        fn = self.function_table.setOverlayAutoCurveDistanceRangeInMeters
        result = fn(ulOverlayHandle, fMinDistanceInMeters, fMaxDistanceInMeters)
        return result

    def getOverlayAutoCurveDistanceRangeInMeters(self, ulOverlayHandle):
        """
        For high-quality curved overlays only, gets the distance range in meters from the overlay used to automatically curve
        the surface around the viewer.  Min is distance is when the surface will be most curved.  Max is when least curved.
        """

        fn = self.function_table.getOverlayAutoCurveDistanceRangeInMeters
        pfMinDistanceInMeters = c_float()
        pfMaxDistanceInMeters = c_float()
        result = fn(ulOverlayHandle, byref(pfMinDistanceInMeters), byref(pfMaxDistanceInMeters))
        return result, pfMinDistanceInMeters.value, pfMaxDistanceInMeters.value

    def setOverlayTextureColorSpace(self, ulOverlayHandle, eTextureColorSpace):
        """
        Sets the colorspace the overlay texture's data is in.  Defaults to 'auto'.
        If the texture needs to be resolved, you should call SetOverlayTexture with the appropriate colorspace instead.
        """

        fn = self.function_table.setOverlayTextureColorSpace
        result = fn(ulOverlayHandle, eTextureColorSpace)
        return result

    def getOverlayTextureColorSpace(self, ulOverlayHandle):
        "Gets the overlay's current colorspace setting."

        fn = self.function_table.getOverlayTextureColorSpace
        peTextureColorSpace = EColorSpace()
        result = fn(ulOverlayHandle, byref(peTextureColorSpace))
        return result, peTextureColorSpace

    def setOverlayTextureBounds(self, ulOverlayHandle):
        "Sets the part of the texture to use for the overlay. UV Min is the upper left corner and UV Max is the lower right corner."

        fn = self.function_table.setOverlayTextureBounds
        pOverlayTextureBounds = VRTextureBounds_t()
        result = fn(ulOverlayHandle, byref(pOverlayTextureBounds))
        return result, pOverlayTextureBounds

    def getOverlayTextureBounds(self, ulOverlayHandle):
        "Gets the part of the texture to use for the overlay. UV Min is the upper left corner and UV Max is the lower right corner."

        fn = self.function_table.getOverlayTextureBounds
        pOverlayTextureBounds = VRTextureBounds_t()
        result = fn(ulOverlayHandle, byref(pOverlayTextureBounds))
        return result, pOverlayTextureBounds

    def getOverlayRenderModel(self, ulOverlayHandle, pchValue, unBufferSize):
        "Gets render model to draw behind this overlay"

        fn = self.function_table.getOverlayRenderModel
        pColor = HmdColor_t()
        pError = EVROverlayError()
        result = fn(ulOverlayHandle, pchValue, unBufferSize, byref(pColor), byref(pError))
        return result, pColor, pError

    def setOverlayRenderModel(self, ulOverlayHandle, pchRenderModel):
        """
        Sets render model to draw behind this overlay and the vertex color to use, pass null for pColor to match the overlays vertex color. 
        The model is scaled by the same amount as the overlay, with a default of 1m.
        """

        fn = self.function_table.setOverlayRenderModel
        pColor = HmdColor_t()
        result = fn(ulOverlayHandle, pchRenderModel, byref(pColor))
        return result, pColor

    def getOverlayTransformType(self, ulOverlayHandle):
        "Returns the transform type of this overlay."

        fn = self.function_table.getOverlayTransformType
        peTransformType = VROverlayTransformType()
        result = fn(ulOverlayHandle, byref(peTransformType))
        return result, peTransformType

    def setOverlayTransformAbsolute(self, ulOverlayHandle, eTrackingOrigin):
        "Sets the transform to absolute tracking origin."

        fn = self.function_table.setOverlayTransformAbsolute
        pmatTrackingOriginToOverlayTransform = HmdMatrix34_t()
        result = fn(ulOverlayHandle, eTrackingOrigin, byref(pmatTrackingOriginToOverlayTransform))
        return result, pmatTrackingOriginToOverlayTransform

    def getOverlayTransformAbsolute(self, ulOverlayHandle):
        "Gets the transform if it is absolute. Returns an error if the transform is some other type."

        fn = self.function_table.getOverlayTransformAbsolute
        peTrackingOrigin = ETrackingUniverseOrigin()
        pmatTrackingOriginToOverlayTransform = HmdMatrix34_t()
        result = fn(ulOverlayHandle, byref(peTrackingOrigin), byref(pmatTrackingOriginToOverlayTransform))
        return result, peTrackingOrigin, pmatTrackingOriginToOverlayTransform

    def setOverlayTransformTrackedDeviceRelative(self, ulOverlayHandle, unTrackedDevice):
        "Sets the transform to relative to the transform of the specified tracked device."

        fn = self.function_table.setOverlayTransformTrackedDeviceRelative
        pmatTrackedDeviceToOverlayTransform = HmdMatrix34_t()
        result = fn(ulOverlayHandle, unTrackedDevice, byref(pmatTrackedDeviceToOverlayTransform))
        return result, pmatTrackedDeviceToOverlayTransform

    def getOverlayTransformTrackedDeviceRelative(self, ulOverlayHandle):
        "Gets the transform if it is relative to a tracked device. Returns an error if the transform is some other type."

        fn = self.function_table.getOverlayTransformTrackedDeviceRelative
        punTrackedDevice = TrackedDeviceIndex_t()
        pmatTrackedDeviceToOverlayTransform = HmdMatrix34_t()
        result = fn(ulOverlayHandle, byref(punTrackedDevice), byref(pmatTrackedDeviceToOverlayTransform))
        return result, punTrackedDevice, pmatTrackedDeviceToOverlayTransform

    def setOverlayTransformTrackedDeviceComponent(self, ulOverlayHandle, unDeviceIndex, pchComponentName):
        """
        Sets the transform to draw the overlay on a rendermodel component mesh instead of a quad. This will only draw when the system is
        drawing the device. Overlays with this transform type cannot receive mouse events.
        """

        fn = self.function_table.setOverlayTransformTrackedDeviceComponent
        result = fn(ulOverlayHandle, unDeviceIndex, pchComponentName)
        return result

    def getOverlayTransformTrackedDeviceComponent(self, ulOverlayHandle, pchComponentName, unComponentNameSize):
        "Gets the transform information when the overlay is rendering on a component."

        fn = self.function_table.getOverlayTransformTrackedDeviceComponent
        punDeviceIndex = TrackedDeviceIndex_t()
        result = fn(ulOverlayHandle, byref(punDeviceIndex), pchComponentName, unComponentNameSize)
        return result, punDeviceIndex

    def getOverlayTransformOverlayRelative(self, ulOverlayHandle):
        "Gets the transform if it is relative to another overlay. Returns an error if the transform is some other type."

        fn = self.function_table.getOverlayTransformOverlayRelative
        ulOverlayHandleParent = VROverlayHandle_t()
        pmatParentOverlayToOverlayTransform = HmdMatrix34_t()
        result = fn(ulOverlayHandle, byref(ulOverlayHandleParent), byref(pmatParentOverlayToOverlayTransform))
        return result, ulOverlayHandleParent, pmatParentOverlayToOverlayTransform

    def setOverlayTransformOverlayRelative(self, ulOverlayHandle, ulOverlayHandleParent):
        "Sets the transform to relative to the transform of the specified overlay. This overlays visibility will also track the parents visibility"

        fn = self.function_table.setOverlayTransformOverlayRelative
        pmatParentOverlayToOverlayTransform = HmdMatrix34_t()
        result = fn(ulOverlayHandle, ulOverlayHandleParent, byref(pmatParentOverlayToOverlayTransform))
        return result, pmatParentOverlayToOverlayTransform

    def showOverlay(self, ulOverlayHandle):
        "Shows the VR overlay.  For dashboard overlays, only the Dashboard Manager is allowed to call this."

        fn = self.function_table.showOverlay
        result = fn(ulOverlayHandle)
        return result

    def hideOverlay(self, ulOverlayHandle):
        "Hides the VR overlay.  For dashboard overlays, only the Dashboard Manager is allowed to call this."

        fn = self.function_table.hideOverlay
        result = fn(ulOverlayHandle)
        return result

    def isOverlayVisible(self, ulOverlayHandle):
        "Returns true if the overlay is visible."

        fn = self.function_table.isOverlayVisible
        result = fn(ulOverlayHandle)
        return result

    def getTransformForOverlayCoordinates(self, ulOverlayHandle, eTrackingOrigin, coordinatesInOverlay):
        "Get the transform in 3d space associated with a specific 2d point in the overlay's coordinate space (where 0,0 is the lower left). -Z points out of the overlay"

        fn = self.function_table.getTransformForOverlayCoordinates
        pmatTransform = HmdMatrix34_t()
        result = fn(ulOverlayHandle, eTrackingOrigin, coordinatesInOverlay, byref(pmatTransform))
        return result, pmatTransform

    def pollNextOverlayEvent(self, ulOverlayHandle, uncbVREvent):
        """
        Returns true and fills the event with the next event on the overlay's event queue, if there is one. 
        If there are no events this method returns false. uncbVREvent should be the size in bytes of the VREvent_t struct
        """

        fn = self.function_table.pollNextOverlayEvent
        pEvent = VREvent_t()
        result = fn(ulOverlayHandle, byref(pEvent), uncbVREvent)
        return result, pEvent

    def getOverlayInputMethod(self, ulOverlayHandle):
        "Returns the current input settings for the specified overlay."

        fn = self.function_table.getOverlayInputMethod
        peInputMethod = VROverlayInputMethod()
        result = fn(ulOverlayHandle, byref(peInputMethod))
        return result, peInputMethod

    def setOverlayInputMethod(self, ulOverlayHandle, eInputMethod):
        "Sets the input settings for the specified overlay."

        fn = self.function_table.setOverlayInputMethod
        result = fn(ulOverlayHandle, eInputMethod)
        return result

    def getOverlayMouseScale(self, ulOverlayHandle):
        """
        Gets the mouse scaling factor that is used for mouse events. The actual texture may be a different size, but this is
        typically the size of the underlying UI in pixels.
        """

        fn = self.function_table.getOverlayMouseScale
        pvecMouseScale = HmdVector2_t()
        result = fn(ulOverlayHandle, byref(pvecMouseScale))
        return result, pvecMouseScale

    def setOverlayMouseScale(self, ulOverlayHandle):
        """
        Sets the mouse scaling factor that is used for mouse events. The actual texture may be a different size, but this is
        typically the size of the underlying UI in pixels (not in world space).
        """

        fn = self.function_table.setOverlayMouseScale
        pvecMouseScale = HmdVector2_t()
        result = fn(ulOverlayHandle, byref(pvecMouseScale))
        return result, pvecMouseScale

    def computeOverlayIntersection(self, ulOverlayHandle):
        """
        Computes the overlay-space pixel coordinates of where the ray intersects the overlay with the
        specified settings. Returns false if there is no intersection.
        """

        fn = self.function_table.computeOverlayIntersection
        pParams = VROverlayIntersectionParams_t()
        pResults = VROverlayIntersectionResults_t()
        result = fn(ulOverlayHandle, byref(pParams), byref(pResults))
        return result, pParams, pResults

    def handleControllerOverlayInteractionAsMouse(self, ulOverlayHandle, unControllerDeviceIndex):
        """
        Processes mouse input from the specified controller as though it were a mouse pointed at a compositor overlay with the
        specified settings. The controller is treated like a laser pointer on the -z axis. The point where the laser pointer would
        intersect with the overlay is the mouse position, the trigger is left mouse, and the track pad is right mouse. 
        * Return true if the controller is pointed at the overlay and an event was generated.
        """

        fn = self.function_table.handleControllerOverlayInteractionAsMouse
        result = fn(ulOverlayHandle, unControllerDeviceIndex)
        return result

    def isHoverTargetOverlay(self, ulOverlayHandle):
        """
        Returns true if the specified overlay is the hover target. An overlay is the hover target when it is the last overlay "moused over" 
        by the virtual mouse pointer
        """

        fn = self.function_table.isHoverTargetOverlay
        result = fn(ulOverlayHandle)
        return result

    def getGamepadFocusOverlay(self):
        "Returns the current Gamepad focus overlay"

        fn = self.function_table.getGamepadFocusOverlay
        result = fn()
        return result

    def setGamepadFocusOverlay(self, ulNewFocusOverlay):
        "Sets the current Gamepad focus overlay"

        fn = self.function_table.setGamepadFocusOverlay
        result = fn(ulNewFocusOverlay)
        return result

    def setOverlayNeighbor(self, eDirection, ulFrom, ulTo):
        """
        Sets an overlay's neighbor. This will also set the neighbor of the "to" overlay
        to point back to the "from" overlay. If an overlay's neighbor is set to invalid both
        ends will be cleared
        """

        fn = self.function_table.setOverlayNeighbor
        result = fn(eDirection, ulFrom, ulTo)
        return result

    def moveGamepadFocusToNeighbor(self, eDirection, ulFrom):
        """
        Changes the Gamepad focus from one overlay to one of its neighbors. Returns VROverlayError_NoNeighbor if there is no
        neighbor in that direction
        """

        fn = self.function_table.moveGamepadFocusToNeighbor
        result = fn(eDirection, ulFrom)
        return result

    def setOverlayTexture(self, ulOverlayHandle):
        """
        Texture to draw for the overlay. This function can only be called by the overlay's creator or renderer process (see SetOverlayRenderingPid) .
        * OpenGL dirty state:
        glBindTexture
        """

        fn = self.function_table.setOverlayTexture
        pTexture = Texture_t()
        result = fn(ulOverlayHandle, byref(pTexture))
        return result, pTexture

    def clearOverlayTexture(self, ulOverlayHandle):
        "Use this to tell the overlay system to release the texture set for this overlay."

        fn = self.function_table.clearOverlayTexture
        result = fn(ulOverlayHandle)
        return result

    def setOverlayRaw(self, ulOverlayHandle, pvBuffer, unWidth, unHeight, unDepth):
        """
        Separate interface for providing the data as a stream of bytes, but there is an upper bound on data 
        that can be sent. This function can only be called by the overlay's renderer process.
        """

        fn = self.function_table.setOverlayRaw
        result = fn(ulOverlayHandle, pvBuffer, unWidth, unHeight, unDepth)
        return result

    def setOverlayFromFile(self, ulOverlayHandle, pchFilePath):
        """
        Separate interface for providing the image through a filename: can be png or jpg, and should not be bigger than 1920x1080.
        This function can only be called by the overlay's renderer process
        """

        fn = self.function_table.setOverlayFromFile
        result = fn(ulOverlayHandle, pchFilePath)
        return result

    def getOverlayTexture(self, ulOverlayHandle, pNativeTextureRef):
        """
        Get the native texture handle/device for an overlay you have created.
        On windows this handle will be a ID3D11ShaderResourceView with a ID3D11Texture2D bound.
        * The texture will always be sized to match the backing texture you supplied in SetOverlayTexture above.
        * You MUST call ReleaseNativeOverlayHandle() with pNativeTextureHandle once you are done with this texture.
        * pNativeTextureHandle is an OUTPUT, it will be a pointer to a ID3D11ShaderResourceView *.
        pNativeTextureRef is an INPUT and should be a ID3D11Resource *. The device used by pNativeTextureRef will be used to bind pNativeTextureHandle.
        """

        fn = self.function_table.getOverlayTexture
        pNativeTextureHandle = c_void_p()
        pWidth = c_uint32()
        pHeight = c_uint32()
        pNativeFormat = c_uint32()
        pAPIType = ETextureType()
        pColorSpace = EColorSpace()
        pTextureBounds = VRTextureBounds_t()
        result = fn(ulOverlayHandle, byref(pNativeTextureHandle), pNativeTextureRef, byref(pWidth), byref(pHeight), byref(pNativeFormat), byref(pAPIType), byref(pColorSpace), byref(pTextureBounds))
        return result, pNativeTextureHandle.value, pWidth.value, pHeight.value, pNativeFormat.value, pAPIType, pColorSpace, pTextureBounds

    def releaseNativeOverlayHandle(self, ulOverlayHandle, pNativeTextureHandle):
        """
        Release the pNativeTextureHandle provided from the GetOverlayTexture call, this allows the system to free the underlying GPU resources for this object,
        so only do it once you stop rendering this texture.
        """

        fn = self.function_table.releaseNativeOverlayHandle
        result = fn(ulOverlayHandle, pNativeTextureHandle)
        return result

    def getOverlayTextureSize(self, ulOverlayHandle):
        "Get the size of the overlay texture"

        fn = self.function_table.getOverlayTextureSize
        pWidth = c_uint32()
        pHeight = c_uint32()
        result = fn(ulOverlayHandle, byref(pWidth), byref(pHeight))
        return result, pWidth.value, pHeight.value

    def createDashboardOverlay(self, pchOverlayKey, pchOverlayFriendlyName):
        "Creates a dashboard overlay and returns its handle"

        fn = self.function_table.createDashboardOverlay
        pMainHandle = VROverlayHandle_t()
        pThumbnailHandle = VROverlayHandle_t()
        result = fn(pchOverlayKey, pchOverlayFriendlyName, byref(pMainHandle), byref(pThumbnailHandle))
        return result, pMainHandle, pThumbnailHandle

    def isDashboardVisible(self):
        "Returns true if the dashboard is visible"

        fn = self.function_table.isDashboardVisible
        result = fn()
        return result

    def isActiveDashboardOverlay(self, ulOverlayHandle):
        "returns true if the dashboard is visible and the specified overlay is the active system Overlay"

        fn = self.function_table.isActiveDashboardOverlay
        result = fn(ulOverlayHandle)
        return result

    def setDashboardOverlaySceneProcess(self, ulOverlayHandle, unProcessId):
        "Sets the dashboard overlay to only appear when the specified process ID has scene focus"

        fn = self.function_table.setDashboardOverlaySceneProcess
        result = fn(ulOverlayHandle, unProcessId)
        return result

    def getDashboardOverlaySceneProcess(self, ulOverlayHandle):
        "Gets the process ID that this dashboard overlay requires to have scene focus"

        fn = self.function_table.getDashboardOverlaySceneProcess
        punProcessId = c_uint32()
        result = fn(ulOverlayHandle, byref(punProcessId))
        return result, punProcessId.value

    def showDashboard(self, pchOverlayToShow):
        "Shows the dashboard."

        fn = self.function_table.showDashboard
        fn(pchOverlayToShow)

    def getPrimaryDashboardDevice(self):
        "Returns the tracked device that has the laser pointer in the dashboard"

        fn = self.function_table.getPrimaryDashboardDevice
        result = fn()
        return result

    def showKeyboard(self, eInputMode, eLineInputMode, pchDescription, unCharMax, pchExistingText, bUseMinimalMode, uUserValue):
        "Show the virtual keyboard to accept input"

        fn = self.function_table.showKeyboard
        result = fn(eInputMode, eLineInputMode, pchDescription, unCharMax, pchExistingText, bUseMinimalMode, uUserValue)
        return result

    def showKeyboardForOverlay(self, ulOverlayHandle, eInputMode, eLineInputMode, pchDescription, unCharMax, pchExistingText, bUseMinimalMode, uUserValue):
        fn = self.function_table.showKeyboardForOverlay
        result = fn(ulOverlayHandle, eInputMode, eLineInputMode, pchDescription, unCharMax, pchExistingText, bUseMinimalMode, uUserValue)
        return result

    def getKeyboardText(self, pchText, cchText):
        "Get the text that was entered into the text input"

        fn = self.function_table.getKeyboardText
        result = fn(pchText, cchText)
        return result

    def hideKeyboard(self):
        "Hide the virtual keyboard"

        fn = self.function_table.hideKeyboard
        fn()

    def setKeyboardTransformAbsolute(self, eTrackingOrigin):
        "Set the position of the keyboard in world space"

        fn = self.function_table.setKeyboardTransformAbsolute
        pmatTrackingOriginToKeyboardTransform = HmdMatrix34_t()
        fn(eTrackingOrigin, byref(pmatTrackingOriginToKeyboardTransform))
        return pmatTrackingOriginToKeyboardTransform

    def setKeyboardPositionForOverlay(self, ulOverlayHandle, avoidRect):
        "Set the position of the keyboard in overlay space by telling it to avoid a rectangle in the overlay. Rectangle coords have (0,0) in the bottom left"

        fn = self.function_table.setKeyboardPositionForOverlay
        fn(ulOverlayHandle, avoidRect)

    def setOverlayIntersectionMask(self, ulOverlayHandle, unNumMaskPrimitives, unPrimitiveSize):
        """
        Sets a list of primitives to be used for controller ray intersection
        typically the size of the underlying UI in pixels (not in world space).
        """

        fn = self.function_table.setOverlayIntersectionMask
        pMaskPrimitives = VROverlayIntersectionMaskPrimitive_t()
        result = fn(ulOverlayHandle, byref(pMaskPrimitives), unNumMaskPrimitives, unPrimitiveSize)
        return result, pMaskPrimitives

    def getOverlayFlags(self, ulOverlayHandle):
        fn = self.function_table.getOverlayFlags
        pFlags = c_uint32()
        result = fn(ulOverlayHandle, byref(pFlags))
        return result, pFlags.value

    def showMessageOverlay(self, pchText, pchCaption, pchButton0Text, pchButton1Text, pchButton2Text, pchButton3Text):
        "Show the message overlay. This will block and return you a result."

        fn = self.function_table.showMessageOverlay
        result = fn(pchText, pchCaption, pchButton0Text, pchButton1Text, pchButton2Text, pchButton3Text)
        return result



class IVRRenderModels_FnTable(Structure):
    _fields_ = [
        ("loadRenderModel_Async", OPENVR_FNTABLE_CALLTYPE(EVRRenderModelError, c_char_p, POINTER(POINTER(RenderModel_t)))),
        ("freeRenderModel", OPENVR_FNTABLE_CALLTYPE(None, POINTER(RenderModel_t))),
        ("loadTexture_Async", OPENVR_FNTABLE_CALLTYPE(EVRRenderModelError, TextureID_t, POINTER(POINTER(RenderModel_TextureMap_t)))),
        ("freeTexture", OPENVR_FNTABLE_CALLTYPE(None, POINTER(RenderModel_TextureMap_t))),
        ("loadTextureD3D11_Async", OPENVR_FNTABLE_CALLTYPE(EVRRenderModelError, TextureID_t, c_void_p, POINTER(c_void_p))),
        ("loadIntoTextureD3D11_Async", OPENVR_FNTABLE_CALLTYPE(EVRRenderModelError, TextureID_t, c_void_p)),
        ("freeTextureD3D11", OPENVR_FNTABLE_CALLTYPE(None, c_void_p)),
        ("getRenderModelName", OPENVR_FNTABLE_CALLTYPE(c_uint32, c_uint32, c_char_p, c_uint32)),
        ("getRenderModelCount", OPENVR_FNTABLE_CALLTYPE(c_uint32)),
        ("getComponentCount", OPENVR_FNTABLE_CALLTYPE(c_uint32, c_char_p)),
        ("getComponentName", OPENVR_FNTABLE_CALLTYPE(c_uint32, c_char_p, c_uint32, c_char_p, c_uint32)),
        ("getComponentButtonMask", OPENVR_FNTABLE_CALLTYPE(c_uint64, c_char_p, c_char_p)),
        ("getComponentRenderModelName", OPENVR_FNTABLE_CALLTYPE(c_uint32, c_char_p, c_char_p, c_char_p, c_uint32)),
        ("getComponentState", OPENVR_FNTABLE_CALLTYPE(openvr_bool, c_char_p, c_char_p, POINTER(VRControllerState_t), POINTER(RenderModel_ControllerMode_State_t), POINTER(RenderModel_ComponentState_t))),
        ("renderModelHasComponent", OPENVR_FNTABLE_CALLTYPE(openvr_bool, c_char_p, c_char_p)),
        ("getRenderModelThumbnailURL", OPENVR_FNTABLE_CALLTYPE(c_uint32, c_char_p, c_char_p, c_uint32, POINTER(EVRRenderModelError))),
        ("getRenderModelOriginalPath", OPENVR_FNTABLE_CALLTYPE(c_uint32, c_char_p, c_char_p, c_uint32, POINTER(EVRRenderModelError))),
        ("getRenderModelErrorNameFromEnum", OPENVR_FNTABLE_CALLTYPE(c_char_p, EVRRenderModelError)),
    ]


class IVRRenderModels(object):
    def __init__(self):
        version_key = IVRRenderModels_Version
        if not isInterfaceVersionValid(version_key):
            _checkInitError(VRInitError_Init_InterfaceNotFound)
        # Thank you lukexi https://github.com/lukexi/openvr-hs/blob/master/cbits/openvr_capi_helper.c#L9
        fn_key = b"FnTable:" + version_key
        fn_type = IVRRenderModels_FnTable
        fn_table_ptr = cast(getGenericInterface(fn_key), POINTER(fn_type))
        if fn_table_ptr is None:
            raise OpenVRError("Error retrieving VR API for IVRRenderModels")
        self.function_table = fn_table_ptr.contents

    def loadRenderModel_Async(self, pchRenderModelName):
        """
        Loads and returns a render model for use in the application. pchRenderModelName should be a render model name
        from the Prop_RenderModelName_String property or an absolute path name to a render model on disk. 
        * The resulting render model is valid until VR_Shutdown() is called or until FreeRenderModel() is called. When the 
        application is finished with the render model it should call FreeRenderModel() to free the memory associated
        with the model.
        * The method returns VRRenderModelError_Loading while the render model is still being loaded.
        The method returns VRRenderModelError_None once loaded successfully, otherwise will return an error.
        """

        fn = self.function_table.loadRenderModel_Async
        ppRenderModel = POINTER(RenderModel_t)()
        result = fn(pchRenderModelName, byref(ppRenderModel))
        # TODO: Automate this manual translation
        if ppRenderModel:
            model = ppRenderModel.contents
        else:
            model = None
        return result, model

    def freeRenderModel(self):
        """
        Frees a previously returned render model
          It is safe to call this on a null ptr.
        """

        fn = self.function_table.freeRenderModel
        pRenderModel = RenderModel_t()
        fn(byref(pRenderModel))
        return pRenderModel

    def loadTexture_Async(self, textureId):
        "Loads and returns a texture for use in the application."

        fn = self.function_table.loadTexture_Async
        ppTexture = POINTER(RenderModel_TextureMap_t)()
        result = fn(textureId, byref(ppTexture))
        return result, ppTexture

    def freeTexture(self):
        """
        Frees a previously returned texture
          It is safe to call this on a null ptr.
        """

        fn = self.function_table.freeTexture
        pTexture = RenderModel_TextureMap_t()
        fn(byref(pTexture))
        return pTexture

    def loadTextureD3D11_Async(self, textureId, pD3D11Device):
        "Creates a D3D11 texture and loads data into it."

        fn = self.function_table.loadTextureD3D11_Async
        ppD3D11Texture2D = c_void_p()
        result = fn(textureId, pD3D11Device, byref(ppD3D11Texture2D))
        return result, ppD3D11Texture2D.value

    def loadIntoTextureD3D11_Async(self, textureId, pDstTexture):
        "Helper function to copy the bits into an existing texture."

        fn = self.function_table.loadIntoTextureD3D11_Async
        result = fn(textureId, pDstTexture)
        return result

    def freeTextureD3D11(self, pD3D11Texture2D):
        "Use this to free textures created with LoadTextureD3D11_Async instead of calling Release on them."

        fn = self.function_table.freeTextureD3D11
        fn(pD3D11Texture2D)

    def getRenderModelName(self, unRenderModelIndex, pchRenderModelName, unRenderModelNameLen):
        """
        Use this to get the names of available render models.  Index does not correlate to a tracked device index, but
        is only used for iterating over all available render models.  If the index is out of range, this function will return 0.
        Otherwise, it will return the size of the buffer required for the name.
        """

        fn = self.function_table.getRenderModelName
        result = fn(unRenderModelIndex, pchRenderModelName, unRenderModelNameLen)
        return result

    def getRenderModelCount(self):
        "Returns the number of available render models."

        fn = self.function_table.getRenderModelCount
        result = fn()
        return result

    def getComponentCount(self, pchRenderModelName):
        """
        Returns the number of components of the specified render model.
         Components are useful when client application wish to draw, label, or otherwise interact with components of tracked objects.
         Examples controller components:
          renderable things such as triggers, buttons
          non-renderable things which include coordinate systems such as 'tip', 'base', a neutral controller agnostic hand-pose
          If all controller components are enumerated and rendered, it will be equivalent to drawing the traditional render model
          Returns 0 if components not supported, >0 otherwise
        """

        fn = self.function_table.getComponentCount
        result = fn(pchRenderModelName)
        return result

    def getComponentName(self, pchRenderModelName, unComponentIndex, pchComponentName, unComponentNameLen):
        """
        Use this to get the names of available components.  Index does not correlate to a tracked device index, but
        is only used for iterating over all available components.  If the index is out of range, this function will return 0.
        Otherwise, it will return the size of the buffer required for the name.
        """

        fn = self.function_table.getComponentName
        result = fn(pchRenderModelName, unComponentIndex, pchComponentName, unComponentNameLen)
        return result

    def getComponentButtonMask(self, pchRenderModelName, pchComponentName):
        """
        Get the button mask for all buttons associated with this component
          If no buttons (or axes) are associated with this component, return 0
          Note: multiple components may be associated with the same button. Ex: two grip buttons on a single controller.
          Note: A single component may be associated with multiple buttons. Ex: A trackpad which also provides "D-pad" functionality
        """

        fn = self.function_table.getComponentButtonMask
        result = fn(pchRenderModelName, pchComponentName)
        return result

    def getComponentRenderModelName(self, pchRenderModelName, pchComponentName, pchComponentRenderModelName, unComponentRenderModelNameLen):
        """
        Use this to get the render model name for the specified rendermode/component combination, to be passed to LoadRenderModel.
        If the component name is out of range, this function will return 0.
        Otherwise, it will return the size of the buffer required for the name.
        """

        fn = self.function_table.getComponentRenderModelName
        result = fn(pchRenderModelName, pchComponentName, pchComponentRenderModelName, unComponentRenderModelNameLen)
        return result

    def getComponentState(self, pchRenderModelName, pchComponentName):
        """
        Use this to query information about the component, as a function of the controller state.
        * For dynamic controller components (ex: trigger) values will reflect component motions
        For static components this will return a consistent value independent of the VRControllerState_t
        * If the pchRenderModelName or pchComponentName is invalid, this will return false (and transforms will be set to identity).
        Otherwise, return true
        Note: For dynamic objects, visibility may be dynamic. (I.e., true/false will be returned based on controller state and controller mode state )
        """

        fn = self.function_table.getComponentState
        pControllerState = VRControllerState_t()
        pState = RenderModel_ControllerMode_State_t()
        pComponentState = RenderModel_ComponentState_t()
        result = fn(pchRenderModelName, pchComponentName, byref(pControllerState), byref(pState), byref(pComponentState))
        return result, pControllerState, pState, pComponentState

    def renderModelHasComponent(self, pchRenderModelName, pchComponentName):
        "Returns true if the render model has a component with the specified name"

        fn = self.function_table.renderModelHasComponent
        result = fn(pchRenderModelName, pchComponentName)
        return result

    def getRenderModelThumbnailURL(self, pchRenderModelName, pchThumbnailURL, unThumbnailURLLen):
        "Returns the URL of the thumbnail image for this rendermodel"

        fn = self.function_table.getRenderModelThumbnailURL
        peError = EVRRenderModelError()
        result = fn(pchRenderModelName, pchThumbnailURL, unThumbnailURLLen, byref(peError))
        return result, peError

    def getRenderModelOriginalPath(self, pchRenderModelName, pchOriginalPath, unOriginalPathLen):
        """
        Provides a render model path that will load the unskinned model if the model name provided has been replace by the user. If the model
        hasn't been replaced the path value will still be a valid path to load the model. Pass this to LoadRenderModel_Async, etc. to load the
        model.
        """

        fn = self.function_table.getRenderModelOriginalPath
        peError = EVRRenderModelError()
        result = fn(pchRenderModelName, pchOriginalPath, unOriginalPathLen, byref(peError))
        return result, peError

    def getRenderModelErrorNameFromEnum(self, error):
        "Returns a string for a render model error"

        fn = self.function_table.getRenderModelErrorNameFromEnum
        result = fn(error)
        return result



class IVRNotifications_FnTable(Structure):
    _fields_ = [
        ("createNotification", OPENVR_FNTABLE_CALLTYPE(EVRNotificationError, VROverlayHandle_t, c_uint64, EVRNotificationType, c_char_p, EVRNotificationStyle, POINTER(NotificationBitmap_t), POINTER(VRNotificationId))),
        ("removeNotification", OPENVR_FNTABLE_CALLTYPE(EVRNotificationError, VRNotificationId)),
    ]


class IVRNotifications(object):
    """
    Allows notification sources to interact with the VR system
    This current interface is not yet implemented. Do not use yet.
    """

    def __init__(self):
        version_key = IVRNotifications_Version
        if not isInterfaceVersionValid(version_key):
            _checkInitError(VRInitError_Init_InterfaceNotFound)
        # Thank you lukexi https://github.com/lukexi/openvr-hs/blob/master/cbits/openvr_capi_helper.c#L9
        fn_key = b"FnTable:" + version_key
        fn_type = IVRNotifications_FnTable
        fn_table_ptr = cast(getGenericInterface(fn_key), POINTER(fn_type))
        if fn_table_ptr is None:
            raise OpenVRError("Error retrieving VR API for IVRNotifications")
        self.function_table = fn_table_ptr.contents

    def createNotification(self, ulOverlayHandle, ulUserValue, type_, pchText, style):
        """
        Create a notification and enqueue it to be shown to the user.
        An overlay handle is required to create a notification, as otherwise it would be impossible for a user to act on it.
        To create a two-line notification, use a line break ('\n') to split the text into two lines.
        The pImage argument may be NULL, in which case the specified overlay's icon will be used instead.
        """

        fn = self.function_table.createNotification
        pImage = NotificationBitmap_t()
        pNotificationId = VRNotificationId()
        result = fn(ulOverlayHandle, ulUserValue, type_, pchText, style, byref(pImage), byref(pNotificationId))
        return result, pImage, pNotificationId

    def removeNotification(self, notificationId):
        "Destroy a notification, hiding it first if it currently shown to the user."

        fn = self.function_table.removeNotification
        result = fn(notificationId)
        return result



class IVRSettings_FnTable(Structure):
    _fields_ = [
        ("getSettingsErrorNameFromEnum", OPENVR_FNTABLE_CALLTYPE(c_char_p, EVRSettingsError)),
        ("sync", OPENVR_FNTABLE_CALLTYPE(openvr_bool, openvr_bool, POINTER(EVRSettingsError))),
        ("setBool", OPENVR_FNTABLE_CALLTYPE(None, c_char_p, c_char_p, openvr_bool, POINTER(EVRSettingsError))),
        ("setInt32", OPENVR_FNTABLE_CALLTYPE(None, c_char_p, c_char_p, c_int32, POINTER(EVRSettingsError))),
        ("setFloat", OPENVR_FNTABLE_CALLTYPE(None, c_char_p, c_char_p, c_float, POINTER(EVRSettingsError))),
        ("setString", OPENVR_FNTABLE_CALLTYPE(None, c_char_p, c_char_p, c_char_p, POINTER(EVRSettingsError))),
        ("getBool", OPENVR_FNTABLE_CALLTYPE(openvr_bool, c_char_p, c_char_p, POINTER(EVRSettingsError))),
        ("getInt32", OPENVR_FNTABLE_CALLTYPE(c_int32, c_char_p, c_char_p, POINTER(EVRSettingsError))),
        ("getFloat", OPENVR_FNTABLE_CALLTYPE(c_float, c_char_p, c_char_p, POINTER(EVRSettingsError))),
        ("getString", OPENVR_FNTABLE_CALLTYPE(None, c_char_p, c_char_p, c_char_p, c_uint32, POINTER(EVRSettingsError))),
        ("removeSection", OPENVR_FNTABLE_CALLTYPE(None, c_char_p, POINTER(EVRSettingsError))),
        ("removeKeyInSection", OPENVR_FNTABLE_CALLTYPE(None, c_char_p, c_char_p, POINTER(EVRSettingsError))),
    ]


class IVRSettings(object):
    def __init__(self):
        version_key = IVRSettings_Version
        if not isInterfaceVersionValid(version_key):
            _checkInitError(VRInitError_Init_InterfaceNotFound)
        # Thank you lukexi https://github.com/lukexi/openvr-hs/blob/master/cbits/openvr_capi_helper.c#L9
        fn_key = b"FnTable:" + version_key
        fn_type = IVRSettings_FnTable
        fn_table_ptr = cast(getGenericInterface(fn_key), POINTER(fn_type))
        if fn_table_ptr is None:
            raise OpenVRError("Error retrieving VR API for IVRSettings")
        self.function_table = fn_table_ptr.contents

    def getSettingsErrorNameFromEnum(self, eError):
        fn = self.function_table.getSettingsErrorNameFromEnum
        result = fn(eError)
        return result

    def sync(self, bForce):
        "Returns true if file sync occurred (force or settings dirty)"

        fn = self.function_table.sync
        peError = EVRSettingsError()
        result = fn(bForce, byref(peError))
        return result, peError

    def setBool(self, pchSection, pchSettingsKey, bValue):
        fn = self.function_table.setBool
        peError = EVRSettingsError()
        fn(pchSection, pchSettingsKey, bValue, byref(peError))
        return peError

    def setInt32(self, pchSection, pchSettingsKey, nValue):
        fn = self.function_table.setInt32
        peError = EVRSettingsError()
        fn(pchSection, pchSettingsKey, nValue, byref(peError))
        return peError

    def setFloat(self, pchSection, pchSettingsKey, flValue):
        fn = self.function_table.setFloat
        peError = EVRSettingsError()
        fn(pchSection, pchSettingsKey, flValue, byref(peError))
        return peError

    def setString(self, pchSection, pchSettingsKey, pchValue):
        fn = self.function_table.setString
        peError = EVRSettingsError()
        fn(pchSection, pchSettingsKey, pchValue, byref(peError))
        return peError

    def getBool(self, pchSection, pchSettingsKey):
        """
        Users of the system need to provide a proper default in default.vrsettings in the resources/settings/ directory
        of either the runtime or the driver_xxx directory. Otherwise the default will be false, 0, 0.0 or ""
        """

        fn = self.function_table.getBool
        peError = EVRSettingsError()
        result = fn(pchSection, pchSettingsKey, byref(peError))
        return result, peError

    def getInt32(self, pchSection, pchSettingsKey):
        fn = self.function_table.getInt32
        peError = EVRSettingsError()
        result = fn(pchSection, pchSettingsKey, byref(peError))
        return result, peError

    def getFloat(self, pchSection, pchSettingsKey):
        fn = self.function_table.getFloat
        peError = EVRSettingsError()
        result = fn(pchSection, pchSettingsKey, byref(peError))
        return result, peError

    def getString(self, pchSection, pchSettingsKey, pchValue, unValueLen):
        fn = self.function_table.getString
        peError = EVRSettingsError()
        fn(pchSection, pchSettingsKey, pchValue, unValueLen, byref(peError))
        return peError

    def removeSection(self, pchSection):
        fn = self.function_table.removeSection
        peError = EVRSettingsError()
        fn(pchSection, byref(peError))
        return peError

    def removeKeyInSection(self, pchSection, pchSettingsKey):
        fn = self.function_table.removeKeyInSection
        peError = EVRSettingsError()
        fn(pchSection, pchSettingsKey, byref(peError))
        return peError



class IVRScreenshots_FnTable(Structure):
    _fields_ = [
        ("requestScreenshot", OPENVR_FNTABLE_CALLTYPE(EVRScreenshotError, POINTER(ScreenshotHandle_t), EVRScreenshotType, c_char_p, c_char_p)),
        ("hookScreenshot", OPENVR_FNTABLE_CALLTYPE(EVRScreenshotError, POINTER(EVRScreenshotType), c_int)),
        ("getScreenshotPropertyType", OPENVR_FNTABLE_CALLTYPE(EVRScreenshotType, ScreenshotHandle_t, POINTER(EVRScreenshotError))),
        ("getScreenshotPropertyFilename", OPENVR_FNTABLE_CALLTYPE(c_uint32, ScreenshotHandle_t, EVRScreenshotPropertyFilenames, c_char_p, c_uint32, POINTER(EVRScreenshotError))),
        ("updateScreenshotProgress", OPENVR_FNTABLE_CALLTYPE(EVRScreenshotError, ScreenshotHandle_t, c_float)),
        ("takeStereoScreenshot", OPENVR_FNTABLE_CALLTYPE(EVRScreenshotError, POINTER(ScreenshotHandle_t), c_char_p, c_char_p)),
        ("submitScreenshot", OPENVR_FNTABLE_CALLTYPE(EVRScreenshotError, ScreenshotHandle_t, EVRScreenshotType, c_char_p, c_char_p)),
    ]


class IVRScreenshots(object):
    "Allows the application to generate screenshots"

    def __init__(self):
        version_key = IVRScreenshots_Version
        if not isInterfaceVersionValid(version_key):
            _checkInitError(VRInitError_Init_InterfaceNotFound)
        # Thank you lukexi https://github.com/lukexi/openvr-hs/blob/master/cbits/openvr_capi_helper.c#L9
        fn_key = b"FnTable:" + version_key
        fn_type = IVRScreenshots_FnTable
        fn_table_ptr = cast(getGenericInterface(fn_key), POINTER(fn_type))
        if fn_table_ptr is None:
            raise OpenVRError("Error retrieving VR API for IVRScreenshots")
        self.function_table = fn_table_ptr.contents

    def requestScreenshot(self, type_, pchPreviewFilename, pchVRFilename):
        """
        Request a screenshot of the requested type.
         A request of the VRScreenshotType_Stereo type will always
         work. Other types will depend on the underlying application
         support.
         The first file name is for the preview image and should be a
         regular screenshot (ideally from the left eye). The second
         is the VR screenshot in the correct format. They should be
         in the same aspect ratio.  Formats per type:
         VRScreenshotType_Mono: the VR filename is ignored (can be
         nullptr), this is a normal flat single shot.
         VRScreenshotType_Stereo:  The VR image should be a
         side-by-side with the left eye image on the left.
         VRScreenshotType_Cubemap: The VR image should be six square
         images composited horizontally.
         VRScreenshotType_StereoPanorama: above/below with left eye
         panorama being the above image.  Image is typically square
         with the panorama being 2x horizontal.
         
         Note that the VR dashboard will call this function when
         the user presses the screenshot binding (currently System
         Button + Trigger).  If Steam is running, the destination
         file names will be in %TEMP% and will be copied into
         Steam's screenshot library for the running application
         once SubmitScreenshot() is called.
         If Steam is not running, the paths will be in the user's
         documents folder under Documents\SteamVR\Screenshots.
         Other VR applications can call this to initiate a
         screenshot outside of user control.
         The destination file names do not need an extension,
         will be replaced with the correct one for the format
         which is currently .png.
        """

        fn = self.function_table.requestScreenshot
        pOutScreenshotHandle = ScreenshotHandle_t()
        result = fn(byref(pOutScreenshotHandle), type_, pchPreviewFilename, pchVRFilename)
        return result, pOutScreenshotHandle

    def hookScreenshot(self, numTypes):
        """
        Called by the running VR application to indicate that it
         wishes to be in charge of screenshots.  If the
         application does not call this, the Compositor will only
         support VRScreenshotType_Stereo screenshots that will be
         captured without notification to the running app.
         Once hooked your application will receive a
         VREvent_RequestScreenshot event when the user presses the
         buttons to take a screenshot.
        """

        fn = self.function_table.hookScreenshot
        pSupportedTypes = EVRScreenshotType()
        result = fn(byref(pSupportedTypes), numTypes)
        return result, pSupportedTypes

    def getScreenshotPropertyType(self, screenshotHandle):
        """
        When your application receives a
         VREvent_RequestScreenshot event, call these functions to get
         the details of the screenshot request.
        """

        fn = self.function_table.getScreenshotPropertyType
        pError = EVRScreenshotError()
        result = fn(screenshotHandle, byref(pError))
        return result, pError

    def getScreenshotPropertyFilename(self, screenshotHandle, filenameType, pchFilename, cchFilename):
        """
        Get the filename for the preview or vr image (see
         vr::EScreenshotPropertyFilenames).  The return value is
         the size of the string.
        """

        fn = self.function_table.getScreenshotPropertyFilename
        pError = EVRScreenshotError()
        result = fn(screenshotHandle, filenameType, pchFilename, cchFilename, byref(pError))
        return result, pError

    def updateScreenshotProgress(self, screenshotHandle, flProgress):
        """
        Call this if the application is taking the screen shot
         will take more than a few ms processing. This will result
         in an overlay being presented that shows a completion
         bar.
        """

        fn = self.function_table.updateScreenshotProgress
        result = fn(screenshotHandle, flProgress)
        return result

    def takeStereoScreenshot(self, pchPreviewFilename, pchVRFilename):
        """
        Tells the compositor to take an internal screenshot of
         type VRScreenshotType_Stereo. It will take the current
         submitted scene textures of the running application and
         write them into the preview image and a side-by-side file
         for the VR image.
         This is similar to request screenshot, but doesn't ever
         talk to the application, just takes the shot and submits.
        """

        fn = self.function_table.takeStereoScreenshot
        pOutScreenshotHandle = ScreenshotHandle_t()
        result = fn(byref(pOutScreenshotHandle), pchPreviewFilename, pchVRFilename)
        return result, pOutScreenshotHandle

    def submitScreenshot(self, screenshotHandle, type_, pchSourcePreviewFilename, pchSourceVRFilename):
        """
        Submit the completed screenshot.  If Steam is running
         this will call into the Steam client and upload the
         screenshot to the screenshots section of the library for
         the running application.  If Steam is not running, this
         function will display a notification to the user that the
         screenshot was taken. The paths should be full paths with
         extensions.
         File paths should be absolute including extensions.
         screenshotHandle can be k_unScreenshotHandleInvalid if this
         was a new shot taking by the app to be saved and not
         initiated by a user (achievement earned or something)
        """

        fn = self.function_table.submitScreenshot
        result = fn(screenshotHandle, type_, pchSourcePreviewFilename, pchSourceVRFilename)
        return result



class IVRResources_FnTable(Structure):
    _fields_ = [
        ("loadSharedResource", OPENVR_FNTABLE_CALLTYPE(c_uint32, c_char_p, c_char_p, c_uint32)),
        ("getResourceFullPath", OPENVR_FNTABLE_CALLTYPE(c_uint32, c_char_p, c_char_p, c_char_p, c_uint32)),
    ]


class IVRResources(object):
    def __init__(self):
        version_key = IVRResources_Version
        if not isInterfaceVersionValid(version_key):
            _checkInitError(VRInitError_Init_InterfaceNotFound)
        # Thank you lukexi https://github.com/lukexi/openvr-hs/blob/master/cbits/openvr_capi_helper.c#L9
        fn_key = b"FnTable:" + version_key
        fn_type = IVRResources_FnTable
        fn_table_ptr = cast(getGenericInterface(fn_key), POINTER(fn_type))
        if fn_table_ptr is None:
            raise OpenVRError("Error retrieving VR API for IVRResources")
        self.function_table = fn_table_ptr.contents

    def loadSharedResource(self, pchResourceName, pchBuffer, unBufferLen):
        """
        Loads the specified resource into the provided buffer if large enough.
        Returns the size in bytes of the buffer required to hold the specified resource.
        """

        fn = self.function_table.loadSharedResource
        result = fn(pchResourceName, pchBuffer, unBufferLen)
        return result

    def getResourceFullPath(self, pchResourceName, pchResourceTypeDirectory, pchPathBuffer, unBufferLen):
        """
        Provides the full path to the specified resource. Resource names can include named directories for
        drivers and other things, and this resolves all of those and returns the actual physical path. 
        pchResourceTypeDirectory is the subdirectory of resources to look in.
        """

        fn = self.function_table.getResourceFullPath
        result = fn(pchResourceName, pchResourceTypeDirectory, pchPathBuffer, unBufferLen)
        return result




########################
### Expose functions ###
########################

def _checkInitError(error):
    """
    Replace openvr error return code with a python exception
    """
    if error != VRInitError_None:
        shutdown()
        raise OpenVRError("%s (error number %d)" %(getVRInitErrorAsSymbol(error), error))


# Copying VR_Init inline implementation from https://github.com/ValveSoftware/openvr/blob/master/headers/openvr.h
# and from https://github.com/phr00t/jMonkeyVR/blob/master/src/jmevr/input/OpenVR.java
def init(applicationType):
    """
    Finds the active installation of the VR API and initializes it. The provided path must be absolute
    or relative to the current working directory. These are the local install versions of the equivalent
    functions in steamvr.h and will work without a local Steam install.
    
    This path is to the "root" of the VR API install. That's the directory with
    the "drivers" directory and a platform (i.e. "win32") directory in it, not the directory with the DLL itself.
    """
    initInternal(applicationType)
    # Retrieve "System" API
    return VRSystem()


def shutdown():
    """
    unloads vrclient.dll. Any interface pointers from the interface are
    invalid after this point
    """
    shutdownInternal() # OK, this is just like inline definition in openvr.h


_openvr.VR_IsHmdPresent.restype = openvr_bool
_openvr.VR_IsHmdPresent.argtypes = []
def isHmdPresent():
    """
    Returns true if there is an HMD attached. This check is as lightweight as possible and
    can be called outside of VR_Init/VR_Shutdown. It should be used when an application wants
    to know if initializing VR is a possibility but isn't ready to take that step yet.
    """
    result =     _openvr.VR_IsHmdPresent()
    return result


_openvr.VR_IsRuntimeInstalled.restype = openvr_bool
_openvr.VR_IsRuntimeInstalled.argtypes = []
def isRuntimeInstalled():
    """
    Returns true if the OpenVR runtime is installed.
    """
    result =     _openvr.VR_IsRuntimeInstalled()
    return result


_openvr.VR_RuntimePath.restype = c_char_p
_openvr.VR_RuntimePath.argtypes = []
def runtimePath():
    """
    Returns where the OpenVR runtime is installed.
    """
    result =     _openvr.VR_RuntimePath()
    return result


_openvr.VR_GetVRInitErrorAsSymbol.restype = c_char_p
_openvr.VR_GetVRInitErrorAsSymbol.argtypes = [EVRInitError]
def getVRInitErrorAsSymbol(error):
    """
    Returns the name of the enum value for an EVRInitError. This function may be called outside of VR_Init()/VR_Shutdown().
    """
    result =     _openvr.VR_GetVRInitErrorAsSymbol(error)
    return result


_openvr.VR_GetVRInitErrorAsEnglishDescription.restype = c_char_p
_openvr.VR_GetVRInitErrorAsEnglishDescription.argtypes = [EVRInitError]
def getVRInitErrorAsEnglishDescription(error):
    """
    Returns an English string for an EVRInitError. Applications should call VR_GetVRInitErrorAsSymbol instead and
    use that as a key to look up their own localized error message. This function may be called outside of VR_Init()/VR_Shutdown().
    """
    result =     _openvr.VR_GetVRInitErrorAsEnglishDescription(error)
    return result


_openvr.VR_GetGenericInterface.restype = c_void_p
_openvr.VR_GetGenericInterface.argtypes = [c_char_p, POINTER(EVRInitError)]
def getGenericInterface(interfaceVersion):
    """
    Returns the interface of the specified version. This method must be called after VR_Init. The
    pointer returned is valid until VR_Shutdown is called.
    """
    error = EVRInitError()
    result =     _openvr.VR_GetGenericInterface(interfaceVersion, byref(error))
    _checkInitError(error.value)
    return result


_openvr.VR_IsInterfaceVersionValid.restype = openvr_bool
_openvr.VR_IsInterfaceVersionValid.argtypes = [c_char_p]
def isInterfaceVersionValid(interfaceVersion):
    """
    Returns whether the interface of the specified version exists.
    """
    result =     _openvr.VR_IsInterfaceVersionValid(interfaceVersion)
    return result


_openvr.VR_GetInitToken.restype = c_uint32
_openvr.VR_GetInitToken.argtypes = []
def getInitToken():
    """
    Returns a token that represents whether the VR interface handles need to be reloaded
    """
    result =     _openvr.VR_GetInitToken()
    return result


_openvr.VR_InitInternal.restype = c_uint32
_openvr.VR_InitInternal.argtypes = [POINTER(EVRInitError), EVRApplicationType]
def initInternal(eApplicationType):
    error = EVRInitError()
    result =     _openvr.VR_InitInternal(byref(error), eApplicationType)
    _checkInitError(error.value)
    return result


_openvr.VR_ShutdownInternal.restype = None
_openvr.VR_ShutdownInternal.argtypes = []
def shutdownInternal():
        _openvr.VR_ShutdownInternal()


