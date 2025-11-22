package com.lloyds.insiderrisk.service;

import com.lloyds.insiderrisk.model.RiskEvent;
import com.lloyds.insiderrisk.repository.RiskEventRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class RiskEventService {

    @Autowired
    private RiskEventRepository riskEventRepository;

    public List<RiskEvent> getEvents(int limit, String riskLevel) {
        if (riskLevel != null && !riskLevel.isEmpty()) {
            return riskEventRepository.findByRiskLevelOrderByTimestampDesc(riskLevel, limit);
        }
        return riskEventRepository.findTopNOrderByTimestampDesc(limit);
    }

    public Optional<RiskEvent> getEventById(Long id) {
        return riskEventRepository.findById(id);
    }

    public RiskEvent createEvent(RiskEvent event) {
        return riskEventRepository.save(event);
    }
}

