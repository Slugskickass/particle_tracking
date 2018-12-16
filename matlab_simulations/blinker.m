clear
samples = 1;
c = 1;
frames = 2500;
t = 1:frames;
mask = NaN(11,11);
mask(:,1) = 1;
mask(:,11) = 1;
mask(1,:) = 1;
mask(11,:) = 1;
sigma = 1;
for photons = 50
    c
    for i = 1:samples
        rx = rand(1);
        ry = rand(1);
        blink = zeros(11,11,20);
        r = 0; %make sure get right number of photons
        for j = 1:frames
            r = r + round((photons/frames-floor(photons/frames)),5);
            if r >= 1;
                blink(:,:,j) = (photGauss(floor(photons/frames)+floor(r),[rx,ry],sigma) + round(randn(11,11)+100));
                r = r-floor(r);
            else
                blink(:,:,j) = (photGauss(floor(photons/frames),[rx,ry],sigma) + round(randn(11,11)+100));
            end
        end
        nblink(:,:,i) = sum(blink,3)-frames*100;
        temp = Fitims(nblink(:,:,i));
        temp(1) = 2*pi*temp(1)*temp(3)*temp(5);
        loc(i,1,c) = temp(4)-rx-5.5;
        loc(i,2,c) = temp(2)-ry-5.5;
        background = mask.*nblink(:,:,i);
        background=(background(~isnan(background)));
        cu(i,:,c) = uncertainty(100,temp,std(background));

        r = (photons/frames-floor(photons/frames));
        cleanBlink = photGauss(floor(photons/frames),[rx,ry],sigma);
        blink(:,:,1) = (cleanBlink + round(randn(11,11)));
        n = floor(photons/frames);
        for j = 2:frames
            r = r + round((photons/frames-floor(photons/frames)),5);
            if r >= 1;
                cleanBlink = cleanBlink + photGauss(floor(photons/frames) + floor(r),[rx,ry],sigma);
                blink(:,:,j) = cleanBlink + round(randn(11,11)+2);
                n = n + floor(photons/frames) + floor(r);
                r = r-floor(r);
            else
                cleanBlink = cleanBlink + photGauss(floor(photons/frames),[rx,ry],sigma);
                blink(:,:,j) = cleanBlink + round(randn(11,11)+2);
                n = n + floor(photons/frames);
            end
        end
        for x = 1:11
            for y = 1:11
                vals = squeeze(blink(x,y,:));
                p = polyfit(t,vals.',1);
                fitted(x,y,i) = p(1)*frames;
            end
        end
        temp = Fitims(fitted(:,:,i));
        temp(1) = 2*pi*temp(1)*temp(3)*temp(5);
        floc(i,1,c) = temp(4)-rx-5.5;
        floc(i,2,c) = temp(2)-ry-5.5;
        background = mask.*fitted(:,:,i);
        background=(background(~isnan(background)));
        fu(i,:,c) = uncertainty(100,temp,std(background));
        ndrblink = blink(:,:,end)-blink(:,:,1);
        temp = Fitims(ndrblink);
        temp(1) = 2*pi*temp(1)*temp(3)*temp(5);
        locn(i,1,c) = temp(4)-rx-5.5;
        locn(i,2,c) = temp(2)-ry-5.5;
        background = mask.*ndrblink;
        background=(background(~isnan(background)));
        nu(i,:,c) = uncertainty(100,temp,std(background));
    end
    c = c+1;
end

%%

for i = 1:size(loc,3)
    m(i) = mean([loc(:,1,i);loc(:,2,i)]);
    error(i) = std([loc(:,1,i);loc(:,2,i)]);
    mf(i) = mean([floc(:,1,i);floc(:,2,i)]);
    errorf(i) = std([floc(:,1,i);floc(:,2,i)]);
    errorn(i) = std([locn(:,1,i);locn(:,2,i)]);
    mn(i) = mean([locn(:,1,i);locn(:,2,i)]);
end

errorbar(m,error)
hold on
errorbar(mf,errorf)
errorbar(mn,errorn)

%%

figure
subplot(2,2,1)
imagesc(cleanBlink)
colormap('hot')
subplot(2,2,2)
imagesc(nblink(:,:,1))
colormap('hot')
subplot(2,2,3)
imagesc(blink(:,:,end)-blink(:,:,1))
colormap('hot')
subplot(2,2,4)
imagesc(fitted(:,:,1))
colormap('hot')

%%

for I = 1:size(cu,3)
    m(I) = mean([cu(:,1,I);cu(:,2,I)]);
    error(I) = std([cu(:,1,I);cu(:,2,I)]);
    mf(I) = mean([fu(:,1,I);fu(:,2,I)]);
    errorf(I) = std([fu(:,1,I);fu(:,2,I)]);
    errorn(I) = std([nu(:,1,I);nu(:,2,I)]);
    mn(I) = mean([nu(:,1,I);nu(:,2,I)]);
end
errorbar((m),error)
hold on
errorbar((mf),errorf)
errorbar((mn),errorn)
% axis([0 50 0 20])

%%


