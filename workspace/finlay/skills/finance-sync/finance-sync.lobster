// Finance Sync Pipeline TaskFlow Definition
// This logic manages the 12-step finance lifecycle.

let taskFlow = api.runtime.tasks.flow.fromToolContext(ctx);

// Create the managed flow
let flow = taskFlow.createManaged({
  controllerId: "finance-sync/master-pipeline",
  goal: "Execute 12-step financial sync reconciler",
  currentStep: "01-discovery",
  stateJson: {
    stagingDir: "/home/node/.openclaw/workspace/finlay/skills/finance-sync/finance-staging/" + api.runtime.date.now(),
    runMode: "DUMMY_RUN"
  }
});

function runStep(stepName) {
  return taskFlow.runTask({
    flowId: flow.flowId,
    runtime: "subagent",
    task: `Executing step ${stepName}`,
    status: "running"
  });
}

// Sequence the pipeline (Condensed for TaskFlow integration)
let steps = [
  "01-discovery", "02-download", "03-firefly-discovery", 
  "04-firefly-refresh", "05-deduplication", "06-reconciliation", 
  "07-verification", "09-prepare-upload"
];

for (let step of steps) {
  let task = runStep(step);
  // In a real TaskFlow runtime, events would handle step-by-step state
  // and persistence would occur here.
}

// Manage lifecycle for DUMMY_RUN
taskFlow.setWaiting({
  flowId: flow.flowId,
  expectedRevision: flow.revision,
  currentStep: "await_review",
  stateJson: flow.stateJson,
  waitJson: { kind: "manual_review" }
});
