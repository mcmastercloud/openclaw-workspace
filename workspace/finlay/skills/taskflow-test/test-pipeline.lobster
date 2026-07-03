let taskFlow = api.runtime.tasks.flow.fromToolContext(ctx);

let flow = taskFlow.createManaged({
  controllerId: "finance-sync/taskflow-test",
  goal: "Execute a single-step canary test",
  currentStep: "canary-step",
  stateJson: {
    status: "initialized",
    timestamp: api.runtime.date.now()
  }
});

let canary = taskFlow.runTask({
  flowId: flow.flowId,
  runtime: "acp",
  task: "Canary test task",
  status: "running"
});

taskFlow.finish({
  flowId: flow.flowId,
  expectedRevision: flow.revision,
  stateJson: { status: "completed" }
});
