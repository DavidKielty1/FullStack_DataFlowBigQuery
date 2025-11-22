package com.lloyds.insiderrisk.repository;

import com.lloyds.insiderrisk.model.RiskEvent;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface RiskEventRepository extends JpaRepository<RiskEvent, Long> {
    
    @Query("SELECT e FROM RiskEvent e WHERE e.riskLevel = :riskLevel ORDER BY e.timestamp DESC LIMIT :limit")
    List<RiskEvent> findByRiskLevelOrderByTimestampDesc(@Param("riskLevel") String riskLevel, @Param("limit") int limit);
    
    @Query("SELECT e FROM RiskEvent e ORDER BY e.timestamp DESC LIMIT :limit")
    List<RiskEvent> findTopNOrderByTimestampDesc(@Param("limit") int limit);
}

