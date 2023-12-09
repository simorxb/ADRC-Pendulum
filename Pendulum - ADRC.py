import matplotlib.pyplot as plt
import pycollimator as collimator

# Load token for Collimator from file
token_file = open("token.txt", 'r')
token = token_file.read()

# Load model from Collimator
project_uuid = "221181d1-4494-4cf8-a58a-61345a7aa14c"
collimator.set_auth_token(token, project_uuid)
model = collimator.load_model("Pendulum - ADRC")

# Desired settle time
T_settle = 1

# Controller poles
s_CL = -6/T_settle

# Controller gains
kp = s_CL**2
kd = -2*s_CL

# Observer poles
s_ESO = 10*s_CL

# Observer gains
l1 = -3*s_ESO 
l2 = 3*(s_ESO**2)
l3 = -(s_ESO)**3

# b0 calculated from nominal mass (0.5 kg) and length (1 m)
b0 = 1/(0.5*1**2)

print("kp: ", kp)
print("kd: ", kd)
print("l1: ", l1)
print("l2: ", l2)
print("l3: ", l3)
print("b0: ", b0)

# Create array of mass values for robustness analysis
m_V = [0.1, 0.5, 1.2]

# Create array of results
res_V = []

# Simulate for each mass value and store results in res_V
for m in m_V:
    sim = collimator.run_simulation(model, parameters = {'m': m, 'l1':l1, 'l2':l2, 'l3':l3, 'b0':b0, 'kp':kp, 'kd':kd})
    res = sim.results.to_pandas()
    res_V.append(res)

plt.figure()

# Plot response for each mass value and setpoint in 1st subplot
plt.subplot(3, 1, 1)

for idx in range(len(m_V)):
    plt.plot(res_V[idx].index, res_V[idx]["Pendulum.Theta"], label=f"Mass = {m_V[idx]} kg")

plt.plot(res_V[0].index, res_V[0]["Setpoint_Filter.out_0"], "--", label="Setpoint")
plt.ylabel(r"$\theta$ [deg]")
plt.legend()
plt.grid()

# Plot controller output for each mass value
plt.subplot(3, 1, 2)

for idx in range(len(m_V)):
    plt.plot(res_V[idx].index, res_V[idx]["inv_b0.out_0"], label=f"Mass = {m_V[idx]} kg")

plt.ylabel(r"$\tau$ [Nm]")
plt.legend()
plt.grid()

# Plot Integrator_3.out_0 for each mass value
plt.subplot(3, 1, 3)

for idx in range(len(m_V)):
    plt.plot(res_V[idx].index, res_V[idx]["Integrator_3.out_0"], label=f"Mass = {m_V[idx]} kg")

plt.xlabel("Time [s]")
plt.ylabel("f(t)")
plt.legend()
plt.grid()

# Show plots
plt.show()