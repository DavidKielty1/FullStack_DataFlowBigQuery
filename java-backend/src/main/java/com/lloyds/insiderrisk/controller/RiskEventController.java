package com.lloyds.insiderrisk.controller;

import com.lloyds.insiderrisk.model.RiskEvent;
import com.lloyds.insiderrisk.service.RiskEventService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/events")
@CrossOrigin(origins = "*")
public class RiskEventController {

    @Autowired
    private RiskEventService riskEventService;

    @GetMapping
    public ResponseEntity<List<RiskEvent>> getEvents(
            @RequestParam(defaultValue = "100") int limit,
            @RequestParam(required = false) String riskLevel) {
        List<RiskEvent> events = riskEventService.getEvents(limit, riskLevel);
        return ResponseEntity.ok(events);
    }

    @GetMapping("/{id}")
    public ResponseEntity<RiskEvent> getEventById(@PathVariable Long id) {
        return riskEventService.getEventById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<RiskEvent> createEvent(@RequestBody RiskEvent event) {
        RiskEvent created = riskEventService.createEvent(event);
        return ResponseEntity.ok(created);
    }
}

