%left bottom width height
set(gcf,'Position',[350 100 600 500])

h1=gca;
set(h1,'position',[.15 .18 .7,.6]);




f = imagesc(new_mat);
set(gca,'YDir','normal');





colormap(flipud(hot));
shading interp;

c = colorbar;
c.Label.String = 'Maximal cost of attraction (arbitrary units)';
set(gca,'FontSize',16);
set(gca,'FontName','Helvetica');


xticks(linspace(0,size(new_mat,2),11));
yticks(linspace(0,size(new_mat,1),6));


x_tcks={};
arr = [0:0.1:1];
for i=1:length(arr)
       x_tcks{i} = num2str(arr(i));
end
xticklabels(x_tcks);

y_tcks={};
arr = [0:0.1:0.5];
for i=1:length(arr)
       y_tcks{i} = num2str(arr(i));
end

yticklabels(y_tcks);

%PATCH FOR NO TICK LABELS
set(gca,'xticklabel',[])
set(gca,'yticklabel',[])



xtickangle(30);
ytickangle(30);

xlabel('Likelihood of stress in the next generation');
ylabel('Male frequency in the population');

%writematrix(flipud(new_mat),'heatmap_rawdata.csv')

