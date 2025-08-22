% Parameters
L = 30; E = 3e10; I = 0.1; A = 0.5; rho = 2500; zeta = 0.05; n_modes = 5;
ms = 225; mu = 25; ks = 2e4; cs = 1.5e3; kt = 2e5; % Quarter-car
v = 20; load = 10e3; g = 9.81; % Load influences gravity term, speed v
T = L / v + 0.5; dt = 0.001; tspan = 0:dt:T;

% Modal properties (simply supported beam)
mu_bar = rho * A; EI = E * I;
omega = zeros(n_modes,1); M_modal = zeros(n_modes,1);
for i = 1:n_modes
    omega(i) = (i*pi/L)^2 * sqrt(EI / mu_bar);
    M_modal(i) = mu_bar * L / 2;
end
phi = @(x,i) sin(i*pi*x/L);
dphi = @(x,i) (i*pi/L) * cos(i*pi*x/L);

% State: [q1 dq1 ... qn dqn ys dys yu dyu]
n_states = 2*n_modes + 4;
y0 = zeros(n_states,1); % Initial zero

% ODE function
function dydt = vbi_ode(t, y)
    q = y(1:2:end-4); dq = y(2:2:end-3);
    ys = y(end-3); dys = y(end-2);
    yu = y(end-1); dyu = y(end);
    x_v = v * t;
    if x_v < 0 || x_v > L
        yb = 0; dyb = 0;
        on_bridge = false;
    else
        yb = 0; dyb = 0;
        for i=1:n_modes
            yb = yb + phi(x_v,i) * q(i);
            dyb = dyb + phi(x_v,i) * dq(i);
        end
        on_bridge = true;
    end
    r = 0; dr = 0; % Smooth road; add roughness if needed e.g., 0.01*sin(2*pi*x_v/5)
    Fc = kt * (yu - yb - r); % No tire damping
    dds = -ks/ms * (ys - yu) - cs/ms * (dys - dyu) - g; % Gravity
    ddu = ks/mu * (ys - yu) + cs/mu * (dys - dyu) - kt/mu * (yu - yb - r) - g;
    dydt = zeros(n_states,1);
    for i=1:n_modes
        dydt(2*i-1) = dq(i);
        ddq = -omega(i)^2 * q(i) - 2*zeta*omega(i)*dq(i);
        if on_bridge
            ddq = ddq + phi(x_v,i) * Fc / M_modal(i);
        end
        dydt(2*i) = ddq;
    end
    dydt(end-3) = dys; dydt(end-2) = dds;
    dydt(end-1) = dyu; dydt(end) = ddu;
end

% Solve
[t, y] = ode45(@vbi_ode, tspan, y0);

% Compute axle accel (ddu)
accel = zeros(length(t),1);
for k = 1:length(t)
    [~, temp] = vbi_ode(t(k), y(k,:));
    accel(k) = temp(end);
end

% Plot accel vs time
figure(1); plot(t, accel);
xlabel('Time (s)'); ylabel('Axle Acceleration (m/s²)'); title('Vehicle Axle Acceleration');

% FFT
Fs = 1/dt; L_fft = length(accel); Y = fft(accel);
P2 = abs(Y/L_fft); P1 = P2(1:floor(L_fft/2)+1); P1(2:end-1) = 2*P1(2:end-1);
f = Fs*(0:floor(L_fft/2))/L_fft;
figure(2); plot(f, P1);
xlabel('Frequency (Hz)'); ylabel('Intensity'); title('FFT of Axle Acceleration'); xlim([0 20]);