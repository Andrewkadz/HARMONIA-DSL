mod e8;
use e8::*;
use walkdir::WalkDir;
use std::fs;
use std::path::Path;
use std::time::Instant;

fn main() {
    println!("=== HARMONIA CONTEXT ENGINE (RUST KERNEL) ===");
    println!("Initializing E8 Cognitive Architecture...");

    // 1. Initialize the Brain (Graph)
    let mut knowledge_graph = SigmaThetaGraph::new();
    
    // 2. Initialize Memory
    let mut memory = ThetaOmegaDeltaMemory::new();

    // 3. Scan the Environment (File System)
    let root_dir = "../"; // Scan the parent directory (HARMONIA-DSL)
    println!("Scanning directory: {}", root_dir);
    
    let start_time = Instant::now();
    let mut file_count = 0;

    for entry in WalkDir::new(root_dir).into_iter().filter_map(|e| e.ok()) {
        let path = entry.path();
        if path.is_file() {
            if let Some(ext) = path.extension() {
                let ext_str = ext.to_str().unwrap_or("");
                if ["py", "md", "rs", "txt"].contains(&ext_str) {
                    process_file(path, &mut knowledge_graph, &mut memory);
                    file_count += 1;
                }
            }
        }
    }

    let duration = start_time.elapsed();
    println!("Scan Complete. Processed {} files in {:.2?}", file_count, duration);

    // 4. Run the Context Loop
    println!("\n--- CONTEXT LOOP ---");
    
    // Recall High-Intensity Memories (Stability > 0.8)
    let core_memories = memory.recall(0.8);
    println!("Core Knowledge Nodes (Stability > 0.8):");
    for mem in core_memories {
        println!(" - [RECALLED]: {}", mem);
    }

    println!("\nSystem Status: ONLINE");
    println!("Ready for Gamma-Phase Injection.");
}

fn process_file(path: &Path, graph: &mut SigmaThetaGraph, memory: &mut ThetaOmegaDeltaMemory) {
    let filename = path.file_name().unwrap().to_str().unwrap();
    
    // Calculate Mass (File Size)
    let metadata = fs::metadata(path).unwrap();
    let mass = metadata.len() as f64;
    
    // Calculate Resonance (Dummy Metric for Prototype)
    let resonance = if filename.contains("harmonia") || filename.contains("e8") { 1.0 } else { 0.1 };
    
    // Create a Pulse
    let pulse = XiPulse::new(filename, mass, resonance);
    
    // Add to Graph
    graph.add_node(filename, &format!("Mass: {}", mass));
    
    // Imprint to Memory if Resonance is High
    if resonance > 0.5 {
        memory.imprint(filename, resonance);
    }
    
    // println!("Processed: {} (Mass: {})", filename, mass);
}
