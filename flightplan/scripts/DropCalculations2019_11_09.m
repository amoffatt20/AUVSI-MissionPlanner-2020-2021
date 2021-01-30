function [LAT, LON] = DropCalculations2019_11_09(GPStar1,GPStar2, GPSwpi1,GPSwpi2, CruisingSpd, DropAlt, California, AvgMagWS, AvgDirWS)

    %GPStar = [Latitude, Longitude] of the target you want to hit {degrees} 
    % GPSwpi = [Latitude, Longitude] of the way point immediately before the target in mission planner {degrees}
    % CruisingSpd = [Velocity] airspeed at which the payload will be dropped {knots}
    % DropAlt = Altitude at which the payload will be dropped {meters}
    % California = [1] if tests are in CA, [0] if in Maryland
    % AvgMagWS = [Windspeed] Velocity of the wind {meter/s}
    % AvgDirWS = [Direction] Direction of the wind with Eastward bound = 0 going C.C.W. {degrees}
        
    DropAlt = DropAlt/3.281;                        %Convert feet to meters
    time_freefall = 1;                              %Time in freefall (No parachute), s
    m = 1.81;                                       %Mass, kg
    g = 9.81;                                       %Gravity Constant, m/s^2
    cd1 = 1.05;
    cd2 = 1.4;                                      %Coefficient of Drag, unitless
    s1 = .0587;
    s2 = 1.58;                                      %Cross-sectional Area, m^2
    tspan1 = [0 time_freefall];
    tspan2 = [time_freefall 20];
    if California == 1
        rho = 1.29;                                 %Air density in California, N/m^3
    else
        rho = 1.31;                                 %Air density in Maryland, N/m^3
    end
    k1 = (cd1*rho*s1)/2;                            %Product of Important UGV Parameters, N/m
    k2 = rho*(cd1*s1 + cd2*s2)/2;                   %Product of Important Parachute Parameters, N/m
    init1 = [DropAlt 0];
    
    [t1,z1] = ode45(@(t1,z1) [z1(2); (k1/m)*z1(2).^2 - g], tspan1, init1);
    
    init2 = [z1(end, 1) z1(end, 2)];
    
    [t2,z2] = ode45(@(t2,z2) [z2(2); (k2/m)*z2(2).^2 - g], tspan2, init2);
   
    A = [t2, z2];
    B = (A <= .15);
    C = A(B);
    D = C(1);
    [idx, val] = find(A==D, 1, 'first');
    time_parachute = A(idx);
        
    AvgDirWS = AvgDirWS * pi / 180;                 %Change wind direction from degrees to radians
    AvgMagWS = AvgMagWS / 1.944;                    %Change wind speed from knots to m/s

    % Change in Latitude from approach point to target {radians}, gives the flight path in the Y direction/vertical axis/aka north and south
    dLat = GPStar1 - GPSwpi1;
    
    % Change in Longitude from approach point to target {radians}, gives the flight path in the X direction/horizontal axis/aka east and west
    dLon = GPStar2 - GPSwpi2;
    
    % Change in displacement in the north and east directions {meters}
    GPSChange = LatLonxy(dLat, dLon, California); %calls function below to convert dLat to dnorth and dLon to dEast
    dNorth = GPSChange(1);                                                                                                                          
    dEast = GPSChange(2);
    
    if (dNorth >= 0 && dEast >= 0) % Quadrant 1
        AppDirPL = atan(dNorth / dEast);            %Absolute direction of plane, m/s
    elseif (dNorth >= 0 && dEast <= 0) % Quadrant 2
        AppDirPL = pi + atan(dNorth / dEast);       %Absolute direction of plane, m/s
    elseif (dNorth <= 0 && dEast <= 0) % Quadrant 3
        AppDirPL = pi + atan(dNorth / dEast);       %Absolute direction of plane, m/s
    elseif (dNorth <= 0 && dEast >= 0) % Quadrant 4        
        AppDirPL = 2 * pi + atan(dNorth / dEast);   %Absolute direction of plane, m/s
    end
    
    Vx1 = (CruisingSpd * cos(AppDirPL)) + (AvgMagWS * cos(AvgDirWS));   %Payload Velocity in X-direction/horizontal axis/aka east and west during freefall, m/s
    Vy1 = (CruisingSpd * sin(AppDirPL)) + (AvgMagWS * sin(AvgDirWS));   %Payload Velocity in Y-direction/vertical axis/aka north and south during freefall, m/s
    %V = sqrt((Vx^2)+(Vy^2))
    
    Vx2 = (AvgMagWS * cos(AvgDirWS));   %Payload Velocity in X-direction/horizontal axis/aka east and west during parachute descent, m/s
    Vy2 = (AvgMagWS * sin(AvgDirWS));   %Payload Velocity in Y-direction/vertical axis/aka north and south during parachute descent, m/s
    
    drop_x1 = Vx1 * time_freefall;      %Payload Travel Distance in X-direction/horizontal axis/aka east and west during freefall, m
    drop_y1 = Vy1 * time_freefall;      %Payload Travel Distance in Y-direction/vertical axis/aka north and south during freefall, m
    
    drop_x2 = Vx2 * time_parachute;     %Payload Travel Distance in X-direction/horizontal axis/aka east and west during parachute descent, m
    drop_y2 = Vy2 * time_parachute;     %Payload Travel Distance in Y-direction/vertical axis/aka north and south during parachute descent, m
    
    dist1 = LatLonxymeter(drop_x1, drop_y1, California);    %Convert freefall distances from meters to degrees, Degrees
    dist2 = LatLonxymeter(drop_x2, drop_y2, California);    %Convert parachute descent distances from meters to degrees, Degrees
    
    GPSChangetoLATLON = dist1 + dist2;  %Total displacement, Degrees
    
    LAT = GPStar1-GPSChangetoLATLON(1);                   %Latitude of drop location, Degrees
    LON = GPStar2-GPSChangetoLATLON(2);                   %Longitude of drop location, Degrees
    
    fid=fopen('gpsoutput2.txt','w');
    fprintf(fid, '%f %f \n', [LAT LON]');
    fclose(fid);
end

function GPSChange = LatLonxy(dlat, dlon, California)
if(California == 0) %We are in Maryland, Since 0 means false and 1 means true
     % Change in degrees Latitude for every meter {Deg/meter}
     ChngLat = 1.112684551E5;
     %1/ChngLon =8.987273079E-6                                                         SIMILAR TO ABOVE .....  .07% diff :)
     % Change in degrees Longitude for every meter {Deg/meter}
     ChngLon = 8.750104301E4;
     % 1/ChngLon = 1.14284352E-5    aboveChngLon = 0.0000114353 .                       SIMILAR TO ABOVE.......  0.06% diff
     
     % Displacement of payload {meters}
     GPSChange = [dlat*ChngLat, dlon*ChngLon];
else %We are in California
     % Change in degrees Latitude for every meter {Deg/meter}
     ChngLat = 1.111785102E5;
     %1/ChngLon = 8.994543983E-6     aboveChngLat = 0.0000089931;                     SIMILAR TO ABOVE.............. 0.02% diff                    
                
     % Change in degrees Longitude for every meter {Deg/meter}
     ChngLon = 9.226910619E4; 
     %%1/ChngLon = 1.08378637E-5    aboveChngLon = 0.000010967;                        SIMILAR TO ABOVE........ 1.18%diff                                        
     
     % Displacement of payload {meters}
     GPSChange = [dlat*ChngLat, dlon*ChngLon];
end
end

function GPSChangetoLATLON = LatLonxymeter(x, y, California)
if(California == 0) %We are in Maryland, Since 0 means false and 1 means true
     % Change in meter for every degrees Latitude {meter/Degrees}
     ChngLattoMeter = 1/1.112684551E5;
     
     % Change in meter for every degrees Longitude {meter/Degrees}
     ChngLontoMeter = 1/8.750104301E4;
     
     % Displacement of payload {Degrees}
     GPSChangetoLATLON = [y*ChngLattoMeter, x*ChngLontoMeter];
else %We are in California
     % Change in meter for every degrees Latitude {meter/Degrees}
     ChngLattoMeter = 1/1.111785102E5;
                
     % Change in meter for every degrees Longitude {meter/Degree}
     ChngLontoMeter = 1/9.226910619E4; 
     
     % Displacement of payload {Degrees}
     GPSChangetoLATLON = [y*ChngLattoMeter, x*ChngLontoMeter];
end
end
