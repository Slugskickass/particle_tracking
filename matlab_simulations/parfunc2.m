function [wn,wc,wf] = parfunc2(s,mark)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
nrep = 10;
wn = zeros(nrep,6);
wc = zeros(nrep,6);
wf = zeros(nrep,6);

for rep = 1:nrep
    vari = s;
    nframes = 1000; %number of frames
    
    %sensor info
    sensorwidth = 250;
    sensorheight = 250;
    reset = 10000; %Camera reset period
    cmos_bin_time = 1; %not used

    %create a molecule
    coords = zeros(nframes+1,2);
    coords(1,1) = round(sensorwidth/2);
    coords(1,2) = round(sensorheight/2);
    
    
    pixel = 100; %nm
    diffusion = 7; %um^2/s | YFP tagged small protein (total 40kDa)
    time = 0.0004; %s | time for each iteration
    minit = 1;
    
    photons = 100000; %number of photons/second
    
    counter = 1;
    for i = 1:nframes %update coords, 4*D*deltat*magnification
        coords(counter+1,1) = coords(counter,1) + normrnd(0,4*diffusion*time*((1000/pixel)^2)/minit);
        coords(counter+1,2) = coords(counter,2) + normrnd(0,4*diffusion*time*((1000/pixel)^2)/minit);
        counter = counter + 1;
    end
    
    % Simulate data
    [ NDRsensor, coords] = NDR_SPT2( sensorwidth, sensorheight, coords, nframes, photons, reset, time );
    [ CMOSsensor, coords] = Zyla_spt2( sensorwidth, sensorheight, coords, nframes, photons, time,cmos_bin_time );
    
    exposure = mark(vari);
    %%%%%%%%
    
    posa = zeros(size(NDRsensor,3)-exposure,2);
    cuts = zeros(11,11,round(size(NDRsensor,3)-exposure));
    afit = zeros(size(NDRsensor,3)-exposure,6);
    posafit = zeros(size(NDRsensor,3)-exposure,2);
    fitted = zeros(11,11,size(NDRsensor,3)-exposure);
    cutscmos = zeros(11,11,round(size(CMOSsensor,3)-exposure));
    posc2 = zeros(size(NDRsensor,3)-exposure,2);
    for i = 1:size(NDRsensor,3)-exposure %extract single molecules
        %%%%% NDR CDS
        h = NDRsensor(:,:,i+exposure)-NDRsensor(:,:,i);
        [m,n] = max(h(:));
        [m,n] = ind2sub([sensorwidth,sensorheight],n);
        cuts(:,:,i) = h(m-5:m+5,n-5:n+5);
        posa(i,1) = m+1;
        posa(i,2) = n+1;
        %%%%% Fitting
        block = NDRsensor(m-5:m+5,n-5:n+5,i:i+exposure-1);
        xvals = 1:exposure;
        for x = 1:size(block,1)
            for y = 1:size(block,2)
                vals = squeeze(block(x,y,:));
                p = polyfit(xvals,vals.',1);
                fitted(x,y,i) = p(1)*s;
            end
        end
        posafit(i,1) = m+1;
        posafit(i,2) = n+1;
        %%CMOS SUM
%         h = sum(CMOSsensor(:,:,i:i+exposure),3);
%         [m,n] = max(h(:));
%         [m,n] = ind2sub([sensorwidth,sensorheight],n);
        cutscmos(:,:,i) = h(m-5:m+5,n-5:n+5);
        posc2(i,1) = m+1;
        posc2(i,2) = n+1;
    end
    a = NDR_fit_stack(cuts); %fit
    afit = NDR_fit_stack(fitted); %fit
    c2 = NDR_fit_stack(cutscmos); %fit
    n = exposure/2+1;
    fcomparison = [];
    ncomparison = [];
    ccomparison = [];
    ccomparison(:,1) = coords(n:end-n+1,2)-(c2(:,2)+posc2(:,2)-6.5);
    ccomparison(:,2) = coords(n:end-n+1,1)-(c2(:,4)+posc2(:,1)-6.5);
    ncomparison(:,2) = coords(n:end-n+1,1)-(a(:,4)+posa(:,1)-6.5);
    ncomparison(:,1) = coords(n:end-n+1,2)-(a(:,2)+posa(:,2)-6.5);
    fcomparison(:,2) = coords(n:end-n+1,1)-(afit(:,4)+posafit(:,1)-6.5);
    fcomparison(:,1) = coords(n:end-n+1,2)-(afit(:,2)+posafit(:,2)-6.5);
    tn = hist3(ncomparison, {-1:0.1:1,-1:0.1:1});
    tc = hist3(ccomparison, {-1:0.1:1,-1:0.1:1});
    tf = hist3(fcomparison, {-1:0.1:1,-1:0.1:1});
    wn(rep,:) = Fitims(tn);
    wc(rep,:) = Fitims(tc);
    wf(rep,:) = Fitims(tf);
end
end

