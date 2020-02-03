clear all

%% set default color order. %matlab only provides 7 colors then it'll repeat
co = [0    0.4470    0.7410;
    0.8500    0.3250    0.0980;
    0.9290    0.6940    0.1250;
    0.4940    0.1840    0.5560;
    0.4660    0.6740    0.1880;
    0.3010    0.7450    0.9330;
    0.6350    0.0780    0.1840;
    0.6471    0.3804    0.0510;
    0.7529    0.7765    0.0824;
    0.8471    0.3882    0.7098   
    ];
set(groot,'defaultAxesColorOrder',co)

%%%%%%%%%%%%%%%%%

std = 2;
run = 1;
counter = 1;
Rmin = 0.0005;
 
%% plot unaveraged C(A)
%
%filename = ['replicates_', num2str(std), '_long/',num2str(run),'_', num2str(counter),'_tree_size_shape_sorted_A.txt'];
filename = ['replicates_', num2str(std), '_Rmin_', num2str(Rmin), '/',num2str(run),'_', num2str(counter),'_tree_size_shape_sorted_A.txt'];
AC_data = load(filename);
A_ = AC_data(:,1);
C_ = AC_data(:,2);
clear AC_data

fig1 = figure; 
%fig1.Renderer = 'Painters'; % save as vector graph
set(fig1,'resize','off')
set(fig1,'PaperUnit','inches')
set(fig1,'PaperSize',[3.375 2.5])
set(fig1,'PaperPositionMode','manual')
set(fig1,'PaperPosition',[0 0 3.375 2.5])

p1 = plot(A_, C_./A_, '.');
set(p1, 'markersize', 1)
set(gca,'fontsize',7);
set(gca, 'xscale', 'log');
set(gca, 'yscale', 'log');
xlabel('A', 'fontsize', 7)
ylabel('C/A', 'fontsize', 7 )
set(gca, 'XTick', (10.^(0:ceil(log10(A_(end))))) );
set(gca, 'YTick', (10.^(0:ceil(log10(C_(end)/A_(end))))) );

%filename = ['replicates_', num2str(std), '_long/',num2str(run),'_', num2str(counter),'_C_A_unaveraged.jpg'];
filename = ['replicates_', num2str(std), '_Rmin_', num2str(Rmin), '/',num2str(run),'_', num2str(counter),'_C_A_unaveraged_linlog_small_dots.jpg'];
print(filename,'-djpeg');
%}

%% plot averaged C(A) and fit for exponent
%
%filename = ['replicates_', num2str(std), '_long/',num2str(run),'_', num2str(counter),'_tree_size_shape_average_A_C.txt'];
%filename = ['replicates_', num2str(std), '_Rmin_', num2str(Rmin), '/',num2str(run),'_', num2str(counter),'_tree_size_shape_average_A_C.txt'];
filename = 'constant/average/AC_average_sigma_5.csv'
AC_data = load(filename);
A_ = AC_data(:,1);
C_ = AC_data(:,2);
clear AC_data

logA = log(A_( A_>10 & A_<200));
logC = log(C_( A_ > 10 & A_<200));
fitp = fitlm(logA, logC); % linear fit

intercept = fitp.Coefficients.Estimate(1); % (1): intercept; (2): the slope
slope = fitp.Coefficients.Estimate(2); % (1): intercept; (2): the slope    
confidence_intervals = coefCI(fitp, 0.05); % 95% confident intervals
slope_CI = confidence_intervals(2,:); % row 2: CI for the slope; row 1: CI for the intercept

fig1 = figure; 
%fig1.Renderer = 'Painters'; % save as vector graph
set(fig1,'resize','off')
set(fig1,'PaperUnit','inches')
set(fig1,'PaperSize',[3.375 2.5])
set(fig1,'PaperPositionMode','manual')
set(fig1,'PaperPosition',[0 0 3.375 2.5])

hold on
p1 = plot(A_, C_./A_, '.');    
p2 = plot( A_, exp( intercept +  log(A_) * slope )./A_ );
hold off
box on
set(p1, 'markersize', 6)
%set(p2, 'linewidth', 1)
set(gca, 'xscale', 'log');
set(gca, 'yscale', 'log');
ylabel('$\bar{C}/A$', 'interpreter', 'latex')
xlabel('$A$', 'interpreter', 'latex') 
set(gca, 'XTick', (10.^(0:ceil(log10(A_(end))))) );
set(gca, 'YTick', (10.^(0:ceil(log10(C_(end)/A_(end))))) );
set(gca, 'fontsize', 7)
%leg = legend('simulation averaged C', sprintf('C ~ A^{%1.3f}, [%1.3f, %1.3f]', [slope, confidence_intervals(2,1),confidence_intervals(2,2)]) );
%legend boxoff
%set(leg, 'fontsize', 6, 'location', 'northwest')

%filename = ['replicates_', num2str(std), '_long/',num2str(run),'_', num2str(counter),'_C_A_averaged_fitted.pdf'];
filename = ['replicates_', num2str(std), '_Rmin_', num2str(Rmin), '/',num2str(run),'_', num2str(counter),'_C_A_averaged_fitted_linlog_small_dots.pdf'];
%print(filename,'-dpdf');
%}