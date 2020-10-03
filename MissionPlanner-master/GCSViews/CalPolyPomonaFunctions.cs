using System;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Globalization;
using System.IO;
using System.Net;
using System.Reflection;
using System.Runtime.Serialization.Formatters.Binary;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml;
using DotSpatial.Data;
using DotSpatial.Projections;
using GeoUtility.GeoSystem;
using GeoUtility.GeoSystem.Base;
using GMap.NET;
using GMap.NET.MapProviders;
using GMap.NET.WindowsForms;
using GMap.NET.WindowsForms.Markers;
using Ionic.Zip;
using log4net;
using MissionPlanner.Controls;
using MissionPlanner.Controls.Waypoints;
using MissionPlanner.Maps;
using MissionPlanner.Properties;
using MissionPlanner.Utilities;
using ProjNet.CoordinateSystems;
using ProjNet.CoordinateSystems.Transformations;
using SharpKml.Base;
using SharpKml.Dom;
using Feature = SharpKml.Dom.Feature;
using ILog = log4net.ILog;
using Placemark = SharpKml.Dom.Placemark;
using Point = System.Drawing.Point;
using Newtonsoft.Json;
using System.Text;
using System.Text.RegularExpressions;
using System.Linq;
using System.Runtime.InteropServices;

namespace MissionPlanner.GCSViews
{
    class CalPolyPomonaFunctions
    {
        public static class InitializeButtons
        {
            public static int DONE { get; set; }
        }
        public static class GuidedModeValue
        {
            public static bool QUIT { get; set; }
            public static int GuidedModeClickCount { get; set; }
            //----------------------------------------------------------
            public static int GuidedModeMissionInitialize { get; set; }
            public static string[] values_mission { get; set; }
            public static int waypoints_total { get; set; }
            //----------------------------------------------------------
            public static int waypoint_next { get; set; }
            public static int waypoint_inprogress { get; set; }
            public static int waypoint_previous { get; set; }
            public static int specific_i { get; set; } //this is for values_mission specific data number
            public static int waypointaccuracy_ft { get; set; }
            public static int Loiter_Check { get; set; }
            public static int waypoint_setdistance { get; set; }
        }
        public static void GuidedModeActual()
        {
            string missionlist = System.IO.File.ReadAllText(@"C:\\Users\\Public\\Downloads\\AUVSI-MissionPlanner-2020-2021\\flightplan\\mission\\MissionPointsParsed.txt");
            GuidedModeValue.values_mission = missionlist.Split(',');
            GuidedModeValue.waypoints_total = GuidedModeValue.values_mission.Length / 4;
        }
        public static void LatLngConversion_toft(bool California, double lat, double lng, out double lat_ft, out double lng_ft)
        {
            lat_ft = 0;
            lng_ft = 0;
            if (California == false) //means we in maryland
            {
                double ChngLat_toMeter = 1 / 1.112684551E5;
                double ChngLon_toMeter = 1 / 8.750104301E4;
                lat_ft = lat * 1 / ChngLat_toMeter * 3.28084;
                lng_ft = lng * 1 / ChngLon_toMeter * 3.28084;
            }
            else //means we in California
            {
                double ChngLat_toMeter = 1 / 1.111785102E5;
                double ChngLon_toMeter = 1 / 9.226910619E4;
                lat_ft = lat * 1 / ChngLat_toMeter * 3.28084;
                lng_ft = lng * 1 / ChngLon_toMeter * 3.28084;
            }
        }
        

    }
}
