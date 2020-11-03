syms p m1 m2 X_c Y_cms Y_cfs f_m Y_ms Y_fs Y_cm Y_cf Y_m Y_f

syms p_m X_s X_cs s2 s3 E_s C V 

V_val = 0.01;



m = p* m1 + (1-p)*m2; %fraction of crossed herms
not_m = p*(1-m1) + (1-p)*(1-m2);


N = m*(X_c+X_cs)+(1-m)*X_s; %MEAN NUMBER OF OFFSPRING

%mean fitness
w_ns = (not_m*X_s/N + m*(X_cs/N))*(f_m*Y_m+(1-f_m)*Y_f)+(m)*(X_c/N)*(0.5*Y_cm+0.5*Y_cf);
w_s = (not_m*X_s/N + m*(X_cs/N))*(f_m*Y_ms+(1-f_m)*Y_fs)+(m)*(X_c/N)*(0.5*Y_cms+0.5*Y_cfs);




p_tag_no_stress = ( 1*p*(p*m1) + 0.5*p*((1-p)*m2) +...
    0.5*(1-p)*(p*m1))*(X_c/N)*(0.5*Y_cm+0.5*Y_cf)+((1-m1)*(X_s/N)+m1*(X_cs/N))*p*(f_m*Y_m+(1-f_m)*Y_f);

p_tag_stress = ( 1*p*(p*m1) + 0.5*p*((1-p)*m2) +...
    0.5*(1-p)*(p*m1))*(X_c/N)*(0.5*Y_cms+0.5*Y_cfs)+((1-m1)*(X_s/N)+m1*(X_cs/N))*p*(f_m*Y_ms+(1-f_m)*Y_fs);


p_tag = E_s*p_tag_stress/w_s+(1-E_s)*p_tag_no_stress/w_ns; 


delta_p = (1-C*V)*p_tag - p;

assert(eval(subs(delta_p,p,0)==0));
%DEBUG
%assert(eval(subs(delta_p,p,1)==0))

diff_delta = diff(delta_p,p);

s_succ = 0.5; 
mtng(p_m,V) = 0.5-0.5*exp(-s_succ*(1+V)*2*p_m/(1-2*p_m));


m1 = mtng(p_m,V_val); %for p (mutant)
m2 = mtng(p_m,0); %for 1-p (all population)

diff_delta_at_zero = subs(diff_delta,p,0);


X_c = 450; %450
X_s = 330; %330
X_cs = 100; %100
f_m = 10^-3;
Y_cm=1;
Y_cf=1;
Y_m=1;
Y_f=1;

Y_cms=1;
Y_cfs=(1-s2);
Y_ms=(1-s3);
Y_fs=(1-s2)*(1-s3);

s2=0.1; %coeff male advantage
s3=0.4; %coeff crossed progeny advantage

V=V_val;
diff_delta_at_zero = subs(subs(diff_delta_at_zero));


eq(E_s,p_m) = subs(diff_delta_at_zero);

Es_arr=[0:0.05:1];
pm_arr=[0:0.05:0.49];

%USE THIS FOR BETTER RESOLUTION OF THE HEATMAP
%Es_arr=[0:0.01:1];
%pm_arr=[0:0.01:0.49];


[Z1,Z2]=meshgrid(Es_arr,pm_arr);
mat = eq(Z1,Z2);


tic

mat_C(C) = mat;
mat_C_0 = mat_C(0);
mat_C_1 = mat_C(1);
new_mat = zeros(size(mat,1),size(mat,2));

toc

tic

for i=1:size(mat,1) %pm_arr
    res=-3; %FOR THE OPTIMIZATION PATCH
    for j=size(mat,2):-1:1 %Es_arr
        
        if res==0 %PATCH FOR SPEED OPTIMIZATION
            break
        end
        
        if mat_C_0(i,j)<=0
            res=0;
        elseif mat_C_1(i,j)>0
            res=1;
        else
            %disp('sol')
            res = vpasolve(mat(i,j),C,[0 1]);
        end
       
        if isempty(res)
            res=3;
        else
            res = res;
        end
        new_mat(i,j) = res;
    end
end
toc


