function [ sensor, coords] = Zyla_spt2( sensorwidth, sensorheight, coords, nframes, maxA, time, bt)
%UNTITLED3 Summary of this function goes here
%   Detailed explanation goes here



NDR_floor = 100;
NDR_noiseInc = 10/100; % calculated for 0.4 ms frame
ResetNoise = 1; % STDev of a single frame at the start of a reset
ReadNoise = 1;
sensor = zeros(sensorwidth,sensorheight,nframes);
sensor(:,:,1) = round((randn(sensorwidth, sensorheight)*ResetNoise)+NDR_floor); %first frame based on noise
[R,C] = ndgrid(1:11, 1:11);
reset_tracker = 1;
counter = 1;
fcounter = 1;
for j = 1:bt:nframes
    %j
    % calculate new frame based on old, plus gaussian noise (not really
    % sure but it seems to work)
    
    sensor(:,:,fcounter+1) = round((randn(sensorwidth, sensorheight)*ResetNoise)+NDR_floor);
    
    
    valmat = photGauss(maxA*time,[coords(counter,1), coords(counter,2)],1); % caluclate blink
    left = uint16(floor(coords(counter,1))-size(R,1)/2); %blink position on surface
    right = uint16(floor(coords(counter,1))+size(R,1)/2-1);
    top = uint16(floor(coords(counter,2))-size(C,1)/2);
    bottom = uint16(floor(coords(counter,2))+size(R,1)/2-1);
    sensor(left:right, top:bottom,fcounter+1) = sensor(left:right, top:bottom,fcounter+1) + valmat; %update sensor
    counter = counter+1;
    fcounter = fcounter + 1;

    
    
end
end

