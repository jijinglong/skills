const eventKinds = new Set(['swing', 'hit', 'block', 'miss']);

function millisecondsToSeconds(value) {
  if (!Number.isFinite(value) || value < 0) {
    throw new RangeError('Hitstop must be a finite number of milliseconds at or above zero');
  }
  return value / 1000;
}

/**
 * Insert contact holds into an action timeline. Times are seconds unless the
 * property explicitly says Ms. Events at the same time share the longest hold.
 */
export function createCombatTimeline({ duration, events, hitstopMs = 105, blockScale = 0.43 }) {
  if (!Number.isFinite(duration) || duration <= 0) {
    throw new RangeError('Duration must be a positive number of seconds');
  }
  if (!Number.isFinite(blockScale) || blockScale < 0) {
    throw new RangeError('Block scale must be a finite non-negative number');
  }

  const hitstop = millisecondsToSeconds(hitstopMs);
  const ordered = [...events].sort((first, second) => first.at - second.at);
  const groups = [];

  for (const event of ordered) {
    if (!eventKinds.has(event.kind) || !Number.isFinite(event.at) || event.at < 0 || event.at > duration) {
      throw new RangeError('Each event needs a valid kind and an action time within the clip');
    }
    const baseHold = event.kind === 'hit' ? hitstop : hitstop * blockScale;
    const contact = event.kind === 'hit' || event.kind === 'block';
    const hold = contact
      ? (event.holdMs === undefined ? baseHold : millisecondsToSeconds(event.holdMs))
      : 0;

    if (groups.at(-1)?.at !== event.at) {
      groups.push({ at: event.at, holdSeconds: 0, events: [] });
    }
    const group = groups.at(-1);
    group.holdSeconds = Math.max(group.holdSeconds, hold);
    group.events.push(event);
  }

  let offset = 0;
  for (const group of groups) {
    group.playbackAt = group.at + offset;
    offset += group.holdSeconds;
  }
  const playbackDuration = duration + offset;

  return {
    duration: playbackDuration,
    events: groups.flatMap(group => group.events.map(event => ({
      ...event,
      playbackAt: group.playbackAt
    }))),

    // Seeking to a contact lands at the start of its hold.
    playbackTimeAt(actionTime) {
      let precedingHold = 0;
      for (const group of groups) {
        if (group.at >= actionTime) break;
        precedingHold += group.holdSeconds;
      }
      return actionTime + precedingHold;
    },

    frameAt(playbackTime) {
      const time = Math.max(0, Math.min(playbackDuration, playbackTime));
      let actionTime = time;
      for (const group of groups) {
        if (group.playbackAt > time) break;
        if (time < group.playbackAt + group.holdSeconds) {
          return { actionTime: group.at, holding: true };
        }
        actionTime -= group.holdSeconds;
      }
      return { actionTime: Math.max(0, Math.min(duration, actionTime)), holding: false };
    }
  };
}
