function [ fits ] = NDR_fit_stack( Image_stack )
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here

[Xs,~,Zs]=size(Image_stack);
XY = Xs;
[X,Y]=meshgrid(1:XY,1:XY); %your x-y coordinates
x(:,1)=X(:); % x= first column
x(:,2)=Y(:); % y= second column
fits  = zeros(Zs,6);


for point_to_use=1:Zs
    Z=reshape(Image_stack(:,:,point_to_use),Xs,Xs);
    if mean(mean(Z)) > 0.1
        options=optimset('Display','off','TolFun',1e-8,'TolX',1e-8,'MaxFunEvals',500);
        %
        %First is scalling
        %Second is X pos
        %Third is X width
        %Fourth is Y pos
        %Fith os Y width
        %6 is offset
        %
        lower=[0,1,1,1,1,0];
        upper=[100000,Xs,10,Xs,10,1000000];
        if min(min(Image_stack(:,:,point_to_use))) < 0
            guesses=[max(max(Image_stack(:,:,point_to_use))),Xs/2,3,Xs/2,3,0];
        else
            guesses=[max(max(Image_stack(:,:,point_to_use))),Xs/2,3,Xs/2,3,min(min(Image_stack(:,:,point_to_use)))];
        end
        
        
        [bestfit,~,~,~]=lsqcurvefit(@Gaussian2D,double(guesses),double(x),double(Z(:)),lower,upper,options);
        
        fits(point_to_use,:) = bestfit;
    end

end

end

