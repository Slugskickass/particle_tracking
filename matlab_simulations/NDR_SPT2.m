function [ sensornoise, coords] = NDR_SPT2( sensorwidth, sensorheight, coords, nframes, maxA, reset, time )
%UNTITLED3 Summary of this function goes here
%   Detailed explanation goes here



NDR_floor = 100;
NDR_noiseInc = 10/100; % calculated for 0.4 ms frame
NDR_rms = 1; % STDev of a single frame at the start of a reset
ReadNoise = 1;
sensorraw = zeros(sensorwidth,sensorheight); %first frame based on noise
sensornoise = zeros(sensorwidth,sensorheight,nframes);
sensornoise(:,:,1) = round((randn(sensorwidth, sensorheight)*NDR_rms)+NDR_floor); %first frame based on noise
[R,C] = ndgrid(1:11, 1:11);
reset_tracker = 1;
counter = 1;
for j = 1:nframes
    if reset_tracker == reset
        sensornoise(:,:,j+1) = round((randn(sensorwidth, sensorheight)*NDR_rms)+NDR_floor);
        reset_tracker = 1;
    else
        reset_tracker = reset_tracker+1;
    end

    %valmat = GaussC(R,C,1, [coords(counter,1), coords(counter,2)], maxA/minit); % caluclate blink
    valmat = photGauss(maxA*time,[coords(counter,1), coords(counter,2)],1);
    left = uint16(floor(coords(j,1))-size(R,1)/2); %blink position on surface
    right = uint16(floor(coords(j,1))+size(R,1)/2-1);
    top = uint16(floor(coords(j,2))-size(C,1)/2);
    bottom = uint16(floor(coords(j,2))+size(R,1)/2-1);
    sensorraw(left:right, top:bottom) = sensorraw(left:right, top:bottom) + valmat; %clean frame to add noise to
    sensornoise(:,:,j+1) = sensornoise(:,:,1) + sensorraw + round((randn(sensorwidth, sensorheight)*ReadNoise))+NDR_noiseInc; %update sensor
    
    counter = counter+1;
    
    
end
end

